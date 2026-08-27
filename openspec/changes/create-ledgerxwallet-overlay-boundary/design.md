# Design: create-ledgerxwallet-overlay-boundary

## Context

`split-openxwallet-repo` was RATIFIED 2026-08-26 and promoted, among others,
`domain-descendant-boundary` — five requirements saying how a DomainxFactory
consumes a neutral `open*` product. Its realization has landed nearly whole:
`opensoft/openXwallet` exists (tags `wallet-v1.0`, `wallet-v1.1`), openxFactory
consumes it at `contract-v2.0` through a nested gitlink plus
`contracts/openxwallet-pin.yaml`, LedgerxFactory re-pointed twice (P5a.2
`be3eead`; P5b `1a8ec62`, PR #30, merge `b131286`), and P3b widened codexFactory's
floor (PR #117, merge `58bd3cf7`, 2026-08-27T21:53). P4 — the aggregation's root
gitlink — is the only wave item still open, and P6 touches no aggregation path.

P6 is the remaining named successor whose gate is already satisfied: descendants
are created LAZILY on the domain's FIRST profile artifact, and LedgerxFactory is
the only domain that has one.

**What P5b left behind is the exact shape of the problem.** The finder in
`tests/validate_wallet_estate.py` narrowed from three candidates to two
(`:53-78`), and both survivors are paths in other repositories reached by walking
up five parents (`:81-116`). Candidate pruning cannot make a directory walk into
a pin. A descendant can.

**This design was narrowed by its own alignment review, and the narrowing is the
main thing to read.** The first draft relocated the estate validator and the
distinct-holder constraint as well as the exercise template. Both were withdrawn
on measured findings — not preferences — and D3 records the measurements, because
a reader who does not see them will propose the withdrawn version again.

## Goals

- Close the rule 1 breach: make `LedgerxWallet` the only path by which the
  Ledgerx domain RESOLVES openXwallet, in tooling and in written procedure.
- Replace a candidate-ordered directory walk with a pin — one fixed path, one
  declared commit.
- Create the boundary with the artifact whose relocation costs nothing, and defer
  the relocations that cost something until their preconditions exist.
- Reduce no coverage, break no prepared procedure, and leave every count and
  lookup in the bar intact.
- Set the precedent for four sibling descendants without creating any of them.

## Non-goals

- Any change to `opensoft/openXwallet` (consumed at `wallet-v1.1`, not re-cut).
- Any change to the xFactory aggregation (D2).
- Moving the tenant estate (Q2), the distinct-holder constraint or the estate
  validator (D3) — all three are successors with stated preconditions.
- Building CI in LedgerxFactory. It has none, and this change does not pretend
  otherwise.
- Promoting `domain-descendant-boundary` into `openspec/specs/`.

## Decisions

### D1 — The pin: MedxChart's shape, stated field by field

**Decision.** `contracts/openxwallet-pin.yaml` carries `schema_version: 1`,
`kind: ledgerxwallet_openxwallet_pin`, `contract_bundle_tag: wallet-v1.1`, and a
`pin:` mapping holding `repository`, `remote`, `revision`, `revision_kind:
commit`, `submodule_path: openXwallet`, `relationship:
pinned_upstream_composition`.

The ratified rule names TWO live examples and they disagree; it derives the KIND
form from both and the FILE shape from neither explicitly. So the shape is stated
here rather than gestured at. `MedxChart/contracts/openchart-pin.yaml:4-10` nests
six fields under a `pin:` mapping; this file **follows that nesting**, carries
**five of the six** (`repository`, `remote`, `revision`, `submodule_path`,
`relationship`), **drops `source_path`** because
`relationship: pinned_upstream_composition` already says the pin covers the whole
tree, and **adds two** (`revision_kind`, `contract_bundle_tag`) because the
ratified rule forbids a tag as the referent and a label must be marked as one.
`MedxAvatar/pins/openavatar.yaml` is not followed — it sits at `pins/`, carries
`source_repo`/`resolved_ref` and no `relationship:`, and the rule settles the
shape "FORWARD only" and forbids reading it as retro-fitting the live files.

The KIND takes `medxchart_openchart_pin`'s compressed form over
`medx_avatar_openavatar_pin`'s underscored one. The rule names both; the corpus
disagrees with itself; the compressed form matches the directory the rule itself
names (`contracts/<product>-pin.yaml`). Recorded so the choice is a decision
rather than a coin toss.

**openxFactory's own pin is the WRONG model, and the parent says why.** That file
uses `kind: pinned_contract_manifest`, `commit:`, `source_repository:`, eight
`sha256:` rows and a `pinned_by_commit_only:` set. Its own design D1 explains the
kind choice: "rule (a)'s `<consumer>_<product>_pin` template governs DESCENDANTS,
and one grammar stretched over both relationships would claim openxFactory is a
wallet descendant." That reasoning runs both ways — LedgerxWallet IS a descendant,
so it takes the descendant grammar.

*Rejected: copying the eight per-file digests.* They are transcribable, and doing
so would give the descendant a content-addressed referent. Rejected because the
descendant consumes openXwallet as a WHOLE TREE through a gitlink — the gitlink
commit is the content address — and a hand-maintained digest list over a tree
nobody enumerates is a second source of truth that drifts silently. The
consequence is real and is stated in § Impact rather than hidden: the Ledgerx
reader becomes gitlink-verified where it was previously reached through
openxFactory's digest-verified gitlink. This CONFORMS (rule 2 asks only for
commit-twice; `neutral-product-pin` is scoped to openxFactory and to required
checks, of which LedgerxFactory has none) but it is a reduction in effect.

**`wallet-v1.1` is an ANNOTATED tag** — object `021cdeef…`, dereferencing to
`63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` (also openXwallet `main` HEAD). The
pin resolves `wallet-v1.1^{commit}`; a bare `rev-parse` would write a tag object
id into a field declared `revision_kind: commit`.

### D2 — Nested-only placement, and the visibility price named

**Decision.** Nested at `LedgerxFactory/LedgerxWallet` — the RATIFIED placement
(`MedxAvatar` in `MedxFactory`, `46f595c6`, 2026-08-23), the one this domain
already realizes for `LedgerxAvatar`. The aggregation's `xFactories/` placement
is not taken.

Three reasons in order of weight. (1) It is the placement whose standing is
RATIFIED; `xFactories/` is REALIZED-BUT-NOT-YET-RATIFIED until
`create-medxchart-overlay-boundary` archives, and a first descendant under a new
standard should not rest its placement on a `Status: draft` act. (2) The
descendant has no standalone-cloning need — the criterion the ratified rule
itself names. (3) It keeps the descendant inside the tree that resolves it, so
the resolution path is a fixed relative path rather than a walk.

**The price, named rather than discovered.** A nested descendant is outside EVERY
governed-repo enumeration in the corpus:
`scripts/sync-notebooklm-books.py:652-653` matches only
`^\s*path\s*=\s*(xFactories/\S+)\s*$`, and its `in_nested_checkout()` (`:629-641`,
skipped at `:767`) excludes any path below a `.git`-carrying directory — so
`xFactories/LedgerxFactory/LedgerxWallet/**` is excluded from LedgerxFactory's OWN
book walk by construction. `scripts/doc_health/ideation_routing.py:225-235`
admits only `openxFactory` and `xFactories/<Name>`. The parent's P4b widens
exactly these two sites by an allowlist of ROOT-LEVEL neutral products, so a
nested domain descendant is outside the set before that widening and after it.
**The ratified precedent is already in this hole** — the aggregation
`.gitmodules` carries no `MedxAvatar` and no `LedgerxAvatar` entry.

Accepted, because the descendant carries a pin, a template and a pin validator
and no ideation corpus. Registered as a successor that would also finally cover
the two existing nested descendants.

*Rejected: taking both placements now.* Permitted by the ratified rule, and it
would buy the visibility above — at the cost of a second gitlink to keep in
lockstep for a repository nobody needs to clone. Two moving parts for a problem
nobody has; the successor can take it when someone does.

### D3 — What moves: the artifact whose move costs nothing

**Decision.** v1 relocates `templates/wallet-exercise.template.yaml` and nothing
else. The distinct-holder constraint, the tenant estate, the estate validator and
the platform seam all stay.

The first draft used a profile/instance TEST — "identical for a second tenant?" —
and moved three files on it. The test is still the right instinct and it is
retained as guidance, but three measurements overrode it, and they are the
substance of this decision.

**M1 — the nested-repository prune.** openXwallet's validator at `wallet-v1.1`
PRUNES NESTED REPOSITORIES from its sweep, by construction and on purpose.
`sweep_candidates()` (`scripts/validate-openxwallet.py:2063`) exists because that
sweep "walks into every repository nested below that root and adjudicates its
carried YAML as LIVE RECORDS of the consumer's tree"; the prune is emitted as a
note at `:2135-2142` ("nested repositories pruned (not adjudicated)"). **So any
wallet-kind YAML placed inside a nested `LedgerxWallet` is adjudicated by
NOTHING.** The prune arrived at P2b of this same parent change, for the
openxFactory case; it applies here unchanged. Moving an adjudicated artifact into
the descendant does not relocate its checking — it ends it.

**M2 — the artifact floor.** `check_real_estate()` runs the pinned validator over
the repository and asserts `elif int(m.group(1)) < 5: err(f"expected >=5
wallet-family records validated …")` (`:721`, `:725-729`). The five are the two
wallet records, the two grants and the distinct-holder constraint. Relocate the
constraint and the count is four; the bar reds on arithmetic.

**M3 — the keyed lookup.** `check_real_estate()` loads all three kinds from
`WALLET_DIR` alone (`:39`, `:735-746`) and then `dhc =
constraints.get(EXPECTED_CONSTRAINT)` → `err(f"missing distinct-holder constraint
…")` (`:774-776`). Relocate the constraint and the lookup returns `None`.

The exercise template is exempt from all three, for a reason its own header
states: it "deliberately carries a template kind instead, because the wallet
validator's repo scan adjudicates any wallet-kind YAML as a live record and a
placeholder record must not be one." Not being adjudicated is its DESIGN, so
relocating it removes nothing from adjudication and changes no count.

**And the template is not tenant-free — the first draft's claim was false.** It
names `grant_ref` (`:24`), `presenting_key_ref` (`:34`), `wallet_ref` (`:38`),
`holder_ref` (`:39`) and `constraint_ref: dhc-lx-create-post-01` (`:48`), and
points instances at `tenants/ledgerxcorp/ledger-estates/` (`:4`). Those are
guidance strings inside placeholder markers, not declared facts. The spec's
refusal is therefore scoped to RECORDS, with an explicit scenario admitting a
template that shows which ids to substitute. Narrowing the rule to fit the
artifact is honest; claiming the artifact fits the rule was not.

**D3a — the seam, and why the test alone gets it wrong.**
`schemas/holder-registry.schema.yaml` would be identical for a second tenant and
still stays: it declares the shape of LedgerLinc table 50200 so "the repo and the
client system state the same facts". Its counterparty is the ENFORCING PLATFORM,
not the pinned product — R3 of the parent one layer down. This is the one named
exception, and naming it is what keeps the test a test.

### D4 — The estate validator stays; only its resolution moves

**Decision.** `tests/validate_wallet_estate.py` remains in LedgerxFactory.
`VALIDATOR_CANDIDATES` (`:53-78`) and the five-level walk in `find_openxfactory()`
(`:81-116`) are replaced by the single fixed relative path
`LedgerxWallet/openXwallet/scripts/validate-openxwallet.py`, resolved from `REPO`,
with the walk DELETED.

**Rule 1 forbids integrating THE PRODUCT'S validator, and this file is not the
product's.** It is LedgerxFactory-authored — its header cites feature 016 and the
2026-08-08 Ledgerx ratification, and features 018 and 019 record it as unpinned
LedgerxFactory code. What breaches rule 1 is where it RESOLVES the product's
validator. Fix the resolution and the breach closes; move the file and the breach
closes too, but four seams open with it.

**The four seams, measured.** `REPO` (`:38`) is used as FOUR different referents:
`WALLET_DIR` (`:39`); the pinned validator's repo-scan target with the `>= 5`
floor (`:721`, `:725-729`); `os.path.join(REPO, "stack.yaml")` →
`yaml.safe_load(fh)["xfactory"]["contract_ref"]` (`:675-676`) — a file
LedgerxWallet has no business owning and never will; and the pin checker's
positional argument (`:705`). And `find_aggregation()` (`:560-595`) is a SECOND
five-level upward walk, hunting a `.gitmodules` naming `openxFactory` so
`check_pin_reconciliation()` can extract the PINNED relocation emitter (`git -C
<openx> show <pin>:scripts/check-openxfactory-pin.py`, `:687-689`) and run it —
a leg the parent's ratified `tasks.md` 6.2 makes this bar the ONLY observer of.
One declared root cannot serve four referents in two repositories, and a
relocation that quietly deepens the second walk shrinks a level budget nobody
re-derived.

Leaving the file where it is makes all of that a non-event. `find_aggregation()`
and `check_pin_reconciliation()` are UNTOUCHED; they concern the openxFactory
BUNDLE pin, a different pin from the one this change is about.

*Rejected: moving it whole, with a delegating bar entry in LedgerxFactory.* The
delegator itself was sound — it is not a fork under rule 3, it carries no rule
that could drift, and the alternatives (widening the `tests/validate_*.py` glob
written down at `docs/protected-surface.md:62` and repeated in three quickstarts;
a symlink, which `os.path.abspath(__file__)` at `:38` does not resolve) are
worse. It was rejected because it is machinery bought to solve a problem this
change need not create.

*Rejected: splitting the validator* — governance half stays, profile half moves.
A real option, and the right shape for the successor. Rejected for v1 because a
split is a refactor of an 822-line file whose five of seven `main()` checks are
implicated, and this change would then be doing a refactor and a boundary in one
act.

**The remediation string is `git submodule update --init --recursive
LedgerxWallet`, plus the path of LedgerxWallet's pin-resync runbook.** Recursive,
because the reader sits two gitlinks down — `LedgerxWallet`, then `openXwallet`
inside it — and a non-recursive init initializes one of the two and leaves the
refusal in place with a command that appeared to succeed. The runbook path is
carried because `neutral-product-pin` requires every fail-closed refusal to name
"the initializing command AND the path of the pin-resync runbook", and a
remediation that names only the command tells the operator how to fetch bytes but
not what to do when the bytes disagree.

**D4a — the finder narrows, and the parent's evidence MIGRATES rather than
dies.** This is the sharpest thing the restructure got wrong on its first pass,
and it is worth stating in full. Deleting `VALIDATOR_CANDIDATES` also deletes:

- `check_finder_candidates()` and its eight `FINDER_PROBES` (`:275-331`),
  including the assertion `if declared != [_NESTED, _AGGREGATION]: err(… "drifted
  from ratified split-openxwallet-repo D9 as narrowed by tasks.md 10.1")` and the
  `legacy-only` probe whose INVERSION the file itself calls "the whole of what
  10.1 changes observably";
- `check_finder_loud_failure()` (`:377-401`), whose docstring names its authority
  as "Ratified split-openxwallet-repo tasks.md 2.3 — 'a loud failure, never a
  skip'";
- the constants `_NESTED`, `_AGGREGATION`, `_LEGACY`, retained at P5b precisely
  "because the valuable fact about this path is now that it must resolve NOTHING".

**Those are the RUNNING realization evidence of the parent's ratified tasks
2.1–2.3 and 10.1, and the parent has NOT archived** — its `tasks.md` 13.1 says
"Fill EVERY cell of the realization-evidence table — it is a gate, not a report."
A P6 that deletes them closes its parent's evidence before its parent's gate.

**Decision: migrate, do not delete, and do not wait.** The ratified PROPERTIES —
declared order, nearer-level-wins, loud failure on nothing found, and the
inverted assertion that a named path resolves NOTHING — all survive the narrowing
as a smaller probe set over the new shape: the single descendant candidate
RESOLVES, and both former candidates plus the pre-carve path resolve NOTHING,
with the loud-failure probe unchanged in intent. `_NESTED` and `_AGGREGATION` are
RETAINED as inverted probes for exactly the reason P5b retained `_LEGACY`. The
migration is a task with the parent's task ids cited in it, so the parent's
evidence table can be filled from P6's run rather than orphaned.

*Rejected: sequencing P6's realization after the parent archives.* It parks a
named successor behind the whole wave's close, including P4, and the parent's own
gate does not wait for P6.

**So `tasks.md` may not say "every negative-probe corpus is byte-unchanged".**
`FINDER_PROBES` is a negative-probe corpus — two of its eight probes assert
`None` — and it cannot survive the narrowing unchanged. The corrected claim names
which corpora are byte-unchanged and which migrate.

### D5 — The descendant ships a validator that actually refuses

**Decision.** LedgerxWallet's scaffold includes `tests/validate_pin.py` and
`.github/workflows/pin-validation.yml` running it.

Ratified rule 2's scenarios say "the descendant's OWN VALIDATOR REFUSES the tree
rather than preferring either" and that a commit moving one declaration without
the other "is refused". A scaffold of a pin file, a gitlink, a README, CODEOWNERS
and a ruleset would ship those refusals DECLARED and nothing that refuses — the
LS-A3 shape, in the requirement's own words.

**It checks FOUR things, and the fourth is the one a declaration-only pin
misses.** (1) `git ls-tree HEAD openXwallet` equals the pin's `revision`;
(2) `revision` is 40 hex and no bare or annotated tag id stands in for it;
(3) `contracts/openxwallet-pin.yaml` and the gitlink moved in the same commit;
and (4) **the CHECKED-OUT `openXwallet/` working tree is at that revision and is
clean** — `git -C openXwallet rev-parse HEAD` plus `git submodule status`
(a leading `+` means the checkout differs from the gitlink). Without (4) the pin
is a declaration with no verifier: a fork of openXwallet, or a stale or dirty
checkout at another commit, EXECUTES while all three recorded declarations still
agree with each other. That is the same "green against a contract version nothing
pins" failure the parent's own candidate ordering exists to prevent, one level in,
and the parent closed its version of it with three checks rather than one.

The pin file therefore also carries `verify_pin: tests/validate_pin.py` and
`resync_runbook: docs/pin-resync-runbook.md`, mirroring openxFactory's own pin
(`:64`, `:60`), and the scaffold includes that runbook — so the refusal has
somewhere to send the operator and the pin names its own verifier rather than
relying on someone knowing where it lives.

The workflow is not decoration: a branch-protection ruleset cannot be promoted
from EVALUATE to ACTIVE until some check has reported, and nothing else in this
change creates one. Without it, task "promote the ruleset" is unsatisfiable.

### D6 — Three declarations of one commit, and exactly what checks them

**Decision.** The invariant is three declarations: LedgerxWallet's gitlink,
LedgerxWallet's pin `revision`, LedgerxFactory's `stack.yaml`
`openxwallet.contract_ref`. (1) and (2) move in the same commit — the ratified
rule — and are checked by D5's validator in the descendant, where the rule puts
the check. (3) is checked by the estate validator when the bar is run: running
code, in a HUMAN-RUN bar, because LedgerxFactory has no workflow at all.

**And the invariant is blind to one drift unless a fourth read is added: WHICH
LedgerxWallet commit.** Nothing in the three declares which descendant commit
LedgerxFactory expects, so a STALE `LedgerxWallet` gitlink checkout yields a
perfectly self-consistent GREEN — the descendant's own pin and gitlink agree with
each other at an old commit, and `stack.yaml` agrees with them because it records
the openXwallet commit rather than the descendant's. So the estate validator's
check reads the descendant's gitlink AS RECORDED BY LedgerxFactory
(`git ls-tree HEAD LedgerxWallet`) and compares it to the descendant checkout it
is about to read — the same `+`-detection D5 applies one level down. Three
declarations of the openXwallet commit, one of the descendant commit; four reads,
not three.

**That is the whole of the enforcement claim.** It is not a required check, and
this design does not describe one. The absence is a named successor.

**Three further declarations exist and are deliberately outside the invariant:**
openxFactory's pin manifest, openxFactory's nested gitlink, and the aggregation's
root gitlink once P4 lands. `neutral-product-pin`'s "consuming repository's pin is
authoritative among reachable checkouts" binds the aggregation-root ↔
openxFactory-nested pair. A THIRD reachable checkout at
`LedgerxFactory/LedgerxWallet/openXwallet` **falls OUTSIDE that rule** — nothing
in the corpus will ever compare the descendant's gitlink to either of the two the
rule covers. Accepted rather than overlooked: they are independent consumers of
one product and may legitimately pin different commits. Such a divergence is NOT
an error and is checked by nothing. An earlier draft called it "REPORTED" and
named no reporter; that sentence was the LS-A3 shape and is gone.

### D7 — `stack.yaml` is a pinned file, and editing it owes a digest re-pin

**Decision.** The `contract_source` edit lands in the same commit as a DIGEST
RE-PIN of `stack.yaml` at `models/protected-surface.yaml:384-385` with a
`pinned_by:` reason naming this change, and the run of
`tests/validate_onboarding_contracts.py` that proves it.

`docs/protected-surface.md:66-70` requires it — "edit it, recompute its digest,
and update the entry with the reason recorded beside it. An unattributed re-pin
defeats the point of pinning" — and the entry itself records what skipping costs
(`:442-445`): "The unpinned window showed as `[baseline] stack.yaml diverges from
its pinned digest` … red on main for seventeen days." P5b re-pinned in the same
commit (`:387-388`).

The first draft asserted "a prose amendment only", which was true of the three
paths it was moving and false of the file it was editing. Recorded as a
correction because the failure mode is documented in the very file being cited.

Separately: the prose pointer is at `:455`, not the `:438` the first draft cited
against a pre-P5b tree. No digest row exists for the relocating template, and
`templates/` is not among `protected_directories` (exactly `credentials`,
`adapters`, `policies`, `openspec/specs`, `conformance`).

### D8 — The prepared live window: repoint and add a precondition

**Decision.** `specs/016-posting-segregation-of-duties/runsheet.md:22-23`,
`quickstart.md:3-7` and `quickstart.md:19` are repointed IN THE SAME COMMIT as
the move, and a **P0.5 precondition** is added naming `git submodule update
--init --recursive LedgerxWallet`.

The runsheet is `Status: prepared (this feature performs NONE of it)` with P0.4
open and phases 1–6 unexecuted; the change that owns it,
`modify-ledgerx-posting-authority-for-segregation-of-duties`, is still ACTIVE and
archives on that window's 6.3. So this is the one place where a topology change
can break something about to be PERFORMED — with a real operator, an ADMIN and an
OPSX lane, minting real keys.

`quickstart.md:19` is also a rule-1 breach site in its own right: it invokes
`python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`
— the neutral validator, by adjacency, out of another repository — and `:3-7`
names that checkout as the prerequisite. Repointing it is not tidying; it is the
same fix as D4 applied to a procedure a human follows. **The first draft cited
`:15` and described it as a relocating profile path; `:15` is the ```sh fence and
the invocation is at `:19`, pointing at the neutral validator. Both the
coordinate and the reason were wrong, and the corrected version makes the repoint
more important rather than less.**

The precondition matters because after the move the operator cannot READ the
template without initializing a submodule, and Phase 0 does not say so.

*Rejected: waiting for the window to close* — it parks P6 behind P0.4, which this
change does not own. *Rejected: repointing later* — a prepared procedure with a
dead link is a broken procedure, and "later" has no owner.

Edits are LINKS AND PREREQUISITES ONLY: no step, actor, abort condition or
evidence requirement is touched.

### D9 — A `git mv` into an empty repository; provenance in prose

**Decision.** The template moves by `git mv` across a repository boundary into a
repository created EMPTY. No `filter-repo`, no history import, no byte-identity
floor.

The parent's P2 needed all three because eight openxFactory-REGISTERED artifacts
and two PROMOTED capabilities were leaving a governed corpus. Nothing of that kind
moves here: the template is LedgerxFactory-authored, carries no openxFactory
manifest row, appears in no `contracts/releases/*.digests.yaml`, and has no digest
row in `models/protected-surface.yaml`.

The obligation that falls out is different: a fresh-repo scaffold loses `git log`,
so LedgerxWallet's `README.md` records the origin repository, the authoring change
(`modify-ledgerx-posting-authority-for-segregation-of-duties`, ratified
2026-08-08), and the LedgerxFactory commit the file came from. Prose provenance is
weaker than history; naming it as weaker is the point.

## Risks and trade-offs

- **A thin first descendant.** v1 ships a pin, one template and a pin validator.
  The boundary — not the volume — is the point: it is what closes rule 1 and what
  the two named successors grow into. But a reviewer is entitled to ask whether a
  repository was needed for one file, and the answer is that the repository is
  needed for the PIN.
- **Gitlink-verified rather than digest-verified** (D1). Conforms; still a
  reduction in effect.
- **Outside every governed-repo enumeration** (D2), alongside the ratified
  precedent.
- **The three-way agreement is checked by a human-run bar, not CI** (D6). If
  nobody runs the bar, nothing catches a disagreement between `stack.yaml` and the
  descendant. This is the packet's most honest weakness.
- **A prepared live window is edited** (D8) — two links, one prerequisite
  paragraph and one new precondition, no steps. The operator must be TOLD, not
  left to discover it.
- **First-of-a-standard risk.** No descendant has previously been created under
  `domain-descendant-boundary`. Whatever this gets wrong is what three more
  domains copy — which is the argument for D3's measurements over D3's instinct,
  and for scoping the spec's creation gate to Ledgerx alone.

## Migration plan

Realization is SPECKIT features, one per `tasks.md` group — OpenSpec ratifies the
boundary, Speckit builds it.

1. **`[OPERATOR]`** Create `opensoft/LedgerxWallet` (private, empty); ruleset in
   EVALUATE mode.
2. Scaffold: README with D9's provenance, `CLAUDE.md`/`AGENTS.md`, CODEOWNERS,
   `tests/validate_pin.py` + its workflow (D5). Add the gitlink at
   `wallet-v1.1^{commit}` AND the pin manifest in ONE commit (D1).
3. Move the template in (D3).
4. **`[LedgerxFactory]`** In ONE commit: the `LedgerxWallet` gitlink and
   `.gitmodules` entry; delete the template; collapse the finder to one fixed path
   with the recursive remediation string (D4); re-source `stack.yaml` (D6) AND
   re-pin its digest (D7); amend the kind registration and the resolution-path
   comment; repoint the runsheet and quickstart and add P0.5 (D8); README and
   CODEOWNERS (`/.gitmodules`, `/LedgerxWallet`).
5. Evidence: the full bar green from an INITIALIZED checkout, with the artifact
   count still 5 and the pin-reconciliation leg still reporting; RED proofs for
   the descendant's pin validator, the uninitialized-submodule refusal, and the
   absence of any resolvable candidate outside the descendant.
6. **`[OPERATOR]`** Promote the ruleset to ACTIVE once `pin-validation` has
   reported; tag `lxw-v1.0`.
7. **`[openxFactory]`** This packet's README Records row and DTN-026's note.

**Rollback** is a reverse `git mv` plus restoring two LedgerxFactory lines and the
digest row. No upstream history is rewritten and no openXwallet content is
touched.

## Open questions

**Q2 — do `tenants/ledgerxcorp/wallets/*` move into LedgerxWallet, or stay as
tenant data?** Recommended: **STAY**, on three grounds of increasing force — the
records are instance data on their own contents; a nested descendant's YAML is
PRUNED from openXwallet's own sweep (M1), so moving them would move them out of
adjudication entirely; and those five files are the commit target of the
runsheet's unexecuted Phase 3.4, a procedure that mints real keys.

This is the one question this packet carries. Everything else is a ratified
constraint, a decision taken and defended, or a correction the packet made to
itself.
