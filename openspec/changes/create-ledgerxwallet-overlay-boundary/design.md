# Design: create-ledgerxwallet-overlay-boundary

## Context

`split-openxwallet-repo` was RATIFIED 2026-08-26 and, among two new
capabilities, promoted `domain-descendant-boundary` — five requirements saying
how a DomainxFactory consumes a neutral `open*` product. Its P1–P5 realization
has landed: `opensoft/openXwallet` exists (created 2026-08-26T23:41:18Z, tags
`wallet-v1.0` and `wallet-v1.1`), openxFactory consumes it at
`contract-v2.0` through a nested gitlink plus
`contracts/openxwallet-pin.yaml`, and LedgerxFactory has re-pointed twice —
P5a.2 (`be3eead`) and P5b (`1a8ec62`, PR #30, merge `b131286`, Speckit feature
`019-openxwallet-consumer-repoints`).

P6 is the remaining named successor and the only one whose gate is already
satisfied: the ratified rules say a descendant is created LAZILY, on the domain's
FIRST profile artifact, and LedgerxFactory is the only domain that has one.

What P5b left behind is the exact shape of the problem. The finder in
`tests/validate_wallet_estate.py` was narrowed from three candidates to two
(`:53-78`), and BOTH survivors are paths in other repositories reached by walking
up five parent directories (`:81-116`). P5b's own note explains why the third was
removed and why restoring it would reintroduce a silent pass. The narrowing is
correct and it is finished: candidate pruning cannot make a directory walk into a
pin. **A descendant can.**

This design is therefore small in surface and specific in shape. It creates one
repository, moves three files, adds one, and edits six paths in one consumer. Its
difficulty is entirely in four places: which artifacts are profile and which are
tenant instances; how the estate keeps its enforcement when the validator leaves;
how many declarations of one commit exist afterwards; and how not to break an
operational procedure that is prepared and about to be performed.

## Goals

- Bring LedgerxFactory into conformance with `domain-descendant-boundary` rule 1
  by making `LedgerxWallet` the only path from the Ledgerx domain to openXwallet.
- Replace a candidate-ordered directory walk with a pin: one deterministic
  validator path, governed by a commit the descendant declares twice.
- Keep the profile/instance line clean, and state it as a decidable test rather
  than as a list of three files.
- Lose no enforcement. The estate is checked after the move by the same rules,
  and the rules exist in exactly one place.
- Break no prepared procedure: the feature-016 live window's references survive
  the relocation.
- Set the precedent for `MedxWallet`, `codexWallet`, `OpsxWallet` and
  `AdxWallet` without creating any of them.

## Non-goals

- Any change to `opensoft/openXwallet`. It is consumed at `wallet-v1.1` and not
  re-cut.
- Any change to the xFactory aggregation. § D2.
- Moving the tenant estate. Q2's recommended disposition is that it stays.
- Moving the platform seam (`schemas/holder-registry.schema.yaml`, the LedgerLinc
  posting surface, BC table 50200).
- Any rename of a `kind:` value, capability id, finding code or filename. R2 of
  the parent freezes the `xfactory_wallet_*` prefix and the profile pins those
  strings by name.
- Promoting `domain-descendant-boundary` into `openspec/specs/`. That happens
  when the parent archives.
- Building CI in LedgerxFactory. It has none today (§ D4), and this change adds
  an invariant plus a runnable bar entry, not a workflow.

## Decisions

### D1 — `contracts/openxwallet-pin.yaml`: MedxChart's shape, not MedxAvatar's

**Decision.** The pin manifest lives at `contracts/openxwallet-pin.yaml` and
carries `schema_version: 1`, `kind: ledgerxwallet_openxwallet_pin`,
`repository: opensoft/openXwallet`, `remote: git@github.com:opensoft/openXwallet.git`,
`revision: <40-hex>`, `revision_kind: commit`, `contract_bundle_tag: wallet-v1.1`,
`submodule_path: openXwallet`, `relationship: pinned_upstream_composition`.

The ratified rule names TWO live examples and they disagree. It derives the kind
form from both (`medxchart_openchart_pin`, `medx_avatar_openavatar_pin`) but the
FILE shape only from one: `MedxChart/contracts/openchart-pin.yaml` carries
`repository`/`remote`/`revision`/`submodule_path`/`source_path`/`relationship`,
while `MedxAvatar/pins/openavatar.yaml` lives at `pins/`, carries
`source_repo`/`resolved_ref`/`resolved_ref_kind` and NO `relationship:`. The rule
settles this "FORWARD only" and says the disagreement "SHALL NOT be read as
retro-fitting them". So the forward shape is MedxChart's, at the directory the
rule NAMES (`contracts/<product>-pin.yaml`), and MedxAvatar is left alone.

`source_path` is omitted rather than set to `.`: the pin covers openXwallet's
whole tree, which is what `relationship: pinned_upstream_composition` already
says, and a redundant field invites a second reading.

**openxFactory's own pin is the WRONG model here, and the parent says so.**
`openxFactory/contracts/openxwallet-pin.yaml` uses `kind:
pinned_contract_manifest`, `commit:`, `source_repository:`, eight `sha256:` rows
and a `pinned_by_commit_only:` set (verified: exactly 8 digest rows). Its own
design D1 explains why it does NOT use a `<consumer>_<product>_pin` kind:
"rule (a)'s `<consumer>_<product>_pin` template governs DESCENDANTS, and one
grammar stretched over both relationships would claim openxFactory is a wallet
descendant." That reasoning runs in both directions. LedgerxWallet IS a
descendant, so it takes the descendant grammar — `ledgerxwallet_openxwallet_pin`,
`repository:`, `revision:` — and not the consumer-direction shape.

*Rejected: a per-file `sha256` block mirroring openxFactory's pin.* openxFactory
pins eight NAMED artifacts it consumes by content, and its verifier
(`scripts/verify-openxwallet-pin.py`) recomputes their digests. LedgerxWallet
consumes openXwallet as a whole tree through a gitlink; the gitlink commit IS the
content address, and a hand-maintained digest list over a tree nobody enumerates
would be a second source of truth that drifts silently. Stated so it can be
contested rather than assumed.

**`wallet-v1.1` is an ANNOTATED tag.** `refs/tags/wallet-v1.1` is tag object
`021cdeefbae50127946f147c23edf98c653aa4a5`, dereferencing to commit
`63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` (also openXwallet's `main` HEAD). The
pin task resolves `wallet-v1.1^{commit}`; recording the bare `rev-parse` output
would write a tag object id into a field declared `revision_kind: commit`.

### D2 — Nested-only placement, and the governance-visibility price it pays

**Decision.** `LedgerxWallet` is nested at `LedgerxFactory/LedgerxWallet` — the
RATIFIED placement (`MedxAvatar` in `MedxFactory`, DTN-022, 2026-08-03), the one
this domain already realizes for `LedgerxAvatar`. The aggregation's `xFactories/`
placement is NOT taken.

Three reasons, in order of weight. (1) It is the placement whose standing is
RATIFIED; `xFactories/` is REALIZED-BUT-NOT-YET-RATIFIED until
`create-medxchart-overlay-boundary` archives, and a first descendant under a new
standard should not rest its placement on a `draft`. (2) The descendant's only
consumer is the tree it is nested in, so there is no standalone-cloning need —
which is the criterion the ratified rule itself names for choosing. (3) Nesting
makes the estate root a fixed relative path (§ D5).

**The price, named rather than discovered later.** openxFactory's governed-repo
enumerations key on `xFactories/<Name>`, and P4b of the parent widens them by an
ALLOWLIST of ROOT-LEVEL neutral products — not by admitting nested gitlinks. So a
nested-only `LedgerxWallet` is outside the notebook projection and the ideation
routing, exactly as `MedxAvatar` has been for five months under the same ratified
placement. **This design accepts that and does not paper over it:** the
descendant carries no ideation corpus (its content is a pin, a profile and a
validator), and if it ever acquires one, the remedy is the `xFactories/` gitlink
or a nested-descendant widening — either of which is a separate change. Recorded
as a risk and as a successor, not as a silent gap.

*Rejected: taking both placements now.* The ratified rule permits it and requires
the two gitlinks to name the same commit. Taking both would buy governance
visibility at the cost of a second gitlink to keep in step, for a repository that
does not yet need cloning — two moving parts to solve a problem nobody has.

### D3 — The profile/instance line, stated as a test

**Decision.** An artifact belongs in `LedgerxWallet` if and only if it would be
IDENTICAL for a second Ledgerx tenant. Everything else is instance data and stays
in `LedgerxFactory`.

That test, not a list, is what the packet is built on — because the next
descendant will face a different set of files and a list does not travel. Applied:

| Artifact | Same for a second tenant? | Home |
| --- | --- | --- |
| `templates/wallet-exercise.template.yaml` | Yes — a stub naming no tenant | LedgerxWallet |
| `dhc-lx-create-post-01.yaml` (distinct-holder constraint) | Yes — `declared_by: ledgerx:posting-segregation-of-duties`, `object_kind: purchase_invoice`, no tenant, no wallet, no key | LedgerxWallet |
| `tests/validate_wallet_estate.py` rules + probe corpora | Yes — domain vocabulary and negative confirmations | LedgerxWallet |
| Custody posture (holder-readable, environment-evidencing, ceiling `act`) | Yes — a domain rule, currently prose-only | LedgerxWallet (§ D8) |
| `wal-lx-*.yaml`, `grant-lx-*.yaml` | **No** — holder ids, DIDs, key ids, `expires_at`, `issued_by`, live `state:` | LedgerxFactory |
| `EXPECTED_WALLETS` / `EXPECTED_GRANTS` (`:147-149`) | **No** — one tenant's ids | LedgerxFactory (§ D6) |
| `schemas/holder-registry.schema.yaml` | Yes across tenants, but its counterparty is Business Central, not openXwallet | LedgerxFactory — § D3a |
| `specs/016`–`019`, `models/protected-surface.yaml` | Records and floors of acts this repo performed | LedgerxFactory |

**D3a — the seam exception, stated because the test alone gets it wrong.** The
holder-registry contract passes the tenant test and still stays. It declares the
shape of LedgerLinc table 50200 so "the repo and the client system state the same
facts"; its counterparty is the ENFORCING PLATFORM, not the pinned product. This
is R3 of the parent applied one layer down — the product owns the standard, the
factory keeps the seam — and it is the ONE named exception to D3's test. Naming it
as an exception is deliberate: an unnamed exception is how a test stops being one.

**The DHC's relocation corrects a mis-filing.** It sits under
`tenants/ledgerxcorp/wallets/` today and names no tenant. Moving it to
`profile/distinct-holder-constraints/` is not a re-scoping and grants no new
authority; `runsheet.md:174` references it BY ID, so the reference survives.

### D4 — The delegating bar entry: one implementation, the glob contract intact

**Decision.** `LedgerxFactory/tests/validate_wallet_estate.py` continues to
EXIST, as a delegating entry of at most a few dozen lines that (a) resolves
`LedgerxWallet/tests/validate_wallet_estate.py` relative to the LedgerxFactory
root, (b) invokes it with this tree as the declared estate root, (c) propagates
its exit code, and (d) REFUSES with a named exit and a remediation string naming
`git submodule update --init LedgerxWallet` when the submodule is uninitialized.
It contains NO rule, NO threshold, NO expected set and NO probe corpus.

**Why the path must survive.** LedgerxFactory has no GitHub Actions workflow at
all — `.github/` holds `CODEOWNERS` and `copilot-instructions.md`. Its estate is
enforced by a human-run glob recorded at `docs/protected-surface.md:62`:
`for f in tests/validate_*.py; do python3 "$f" || echo "FAIL $f"; done`. A plain
`git mv` therefore removes the wallet estate from the ONLY bar that ever checks
it, and — because there is no required check — it does so silently. That is
quieter than a CI break, not safer.

**Why a delegator is not a fork.** Rule 3 forbids "a fork, an edited copy or a
re-authoring of the neutral product's contracts, schemas, corpus or validator".
The delegator re-authors nothing: it holds no rule that could disagree with the
implementation, and the failure mode a fork creates — two answers to the same
question — is unavailable to a file that computes no answer. The property to
preserve is testable and is stated as one: **every rule, threshold, expected set
and probe corpus appears in exactly one file.**

*Rejected: widening the bar glob to reach into the submodule.* The glob is
written down in a promoted-adjacent doc and read by humans; widening it means
every future reader must know that `tests/validate_*.py` is not the whole bar.
*Rejected: a symlink.* It survives neither Windows checkouts nor an
uninitialized submodule with a legible message. *Rejected: keeping the validator
in LedgerxFactory and moving only the template and the DHC.* It is the option the
bench should weigh hardest, and it loses on rule 1: the validator is precisely
the artifact whose RESOLUTION reaches outside the repository, so leaving it
behind leaves the breach in place and buys a smaller diff.

### D5 — One candidate, and an estate root that is declared rather than walked

**Decision.** Inside LedgerxWallet the validator resolves the neutral validator
at ONE fixed relative path, `openXwallet/scripts/validate-openxwallet.py`,
governed by `contracts/openxwallet-pin.yaml` in the same commit. The five-level
upward walk and the candidate tuple are DELETED, not narrowed: after this change
there is nothing to break a tie between.

The scan target is a DECLARED ESTATE ROOT. It is an explicit parameter,
defaulting to the parent directory of the LedgerxWallet checkout, and the
validator REFUSES with a named exit when that root holds no `tenants/*/wallets/`
directory — never a skip, on LedgerxFactory's own repo law of 2026-08-07 that
"an unreadable surface must fail, not degrade to 'empty'".

**The estate root carries THREE jobs, not one — and missing any of them breaks
the move.** The validator's location dependencies are wider than the wallet
estate, and enumerating them is what makes D5 sufficient rather than plausible.
Read on LedgerxFactory `origin/main`:

1. **The estate scan** — `tenants/*/wallets/`, and the `err()` at `:706`
   ("missing estate directory tenants/ledgerxcorp/wallets").
2. **`stack.yaml`** — `check_pin_reconciliation()` opens
   `os.path.join(REPO, "stack.yaml")` and reads
   `yaml.safe_load(fh)["xfactory"]["contract_ref"]`. LedgerxWallet has no
   `stack.yaml` and never will: the domain stack is the DOMAIN's declaration.
   So this read must be re-based on the estate root, not on the module's own
   `REPO`. **This is the dependency a naive `git mv` would break silently at
   import-adjacent time, and it is why D5 says "declared" rather than "walked".**
3. **A SECOND upward walk** — `find_aggregation()` (`:583-594`) climbs five
   parents looking for a `.gitmodules` that mentions `openxFactory`, to locate
   the xFactory AGGREGATION root and, under it, an openxFactory checkout. It then
   extracts the PINNED emitter (`git -C <openx> show
   <xfactory.contract_ref>:scripts/check-openxfactory-pin.py`, `:688`) and runs
   it with the repository and `--aggregation-root`. That is a THIRD repository
   dependency, it is required by the parent's ratified `tasks.md` 6.2, and it
   is about the openxFactory BUNDLE pin — a different pin from the openXwallet
   one this change is otherwise concerned with.

**Decision on each.** (1) and (2) take the estate root. (3) keeps its walk but
starts it from the ESTATE ROOT rather than from the module's own location, so the
level budget is measured from the domain repository exactly as it is today —
otherwise nesting spends one of the five levels and a LedgerxWallet Speckit
worktree spends two, quietly shrinking a budget nobody re-derived. The emitter
invocation continues to pass the DOMAIN repository as its scan target, because
that is the tree whose pin is being reconciled.

**The consequence for the estate-root parameter is that it is not optional.** A
default is a convenience for the nested layout; every one of the three jobs
refuses with a named exit when the root it was given is not a domain repository —
no `tenants/*/wallets/`, no `stack.yaml`, no aggregation above it. Three
refusals, not one, and each names what it could not read.

**LedgerxWallet inherits a PyYAML dependency** (`yaml.safe_load`), so the
scaffold declares it rather than discovering it on the first run.

This is R6 of the parent one layer down. There, the review-authority register
stayed in openxFactory while its READER travelled with the validator, and the
reader was given the scan target as an argument. Here the tenant estate stays in
LedgerxFactory while its validator travels, and takes the estate root the same
way. The rhyme is deliberate and it is the reason the split is safe.

**The relative default has one sharp edge, and it is bounded by D2.** If
LedgerxWallet were ever ALSO aggregated at `xFactories/LedgerxWallet`, `..`
resolves to `xFactories/` — not a Ledgerx tree — and the default would silently
point at nothing. Two guards: the refusal above fires (no `tenants/*/wallets/`
under `xFactories/`), so the failure is loud rather than silent; and D2 does not
take the second placement. If a later change takes it, the default becomes a
required argument. Recorded as a precondition on that change rather than as a
guess here.

### D6 — The expected set moves to the estate that owns the ids

**Decision.** `EXPECTED_WALLETS`, `EXPECTED_GRANTS` and `EXPECTED_CONSTRAINT`
(`:147-150`) do not travel as literals. The two wallet ids and the two grant→
wallet bindings become a declared estate manifest in LedgerxFactory beside the
records they enumerate; the validator READS it and checks the committed estate
against it. `EXPECTED_CONSTRAINT` travels, because after § D3 the constraint IS a
profile artifact and the profile may name its own.

Without this, a cross-tenant profile repository hard-codes one tenant's wallet
ids — the same inversion D3 refuses for the records themselves, smuggled in as
code instead of as data. The mechanical consequence is worth stating: the
validator's assertion changes from "these two ids are present" to "the declared
set and the committed set agree", which is a STRICTLY stronger check, because it
also catches a record added without a declaration.

### D7 — Three declarations of one commit, and what actually checks them

**Decision.** After this change the Ledgerx domain declares the openXwallet
commit in THREE places, and they must agree:

1. `LedgerxWallet/openXwallet` gitlink
2. `LedgerxWallet/contracts/openxwallet-pin.yaml` `revision`
3. `LedgerxFactory/stack.yaml` `openxwallet.contract_ref`

(1) and (2) move in the SAME commit — that is the ratified rule, and it is what
makes the pin one act. (3) is the domain's declared consumption and is re-sourced
from `openxFactory-nested-submodule-pin` to `LedgerxWallet-nested-submodule-pin`,
because after this change the descendant IS how the domain consumes the product.
`contract_ref` itself does not change (`63f5a1ad…`), so the re-homing is
bisectable against a re-pin.

**What checks it, stated exactly, because a described control that nothing runs
is the LS-A3 failure.** The delegating bar entry (§ D4) reads all three and
REFUSES on any disagreement, before it invokes anything. That is running code in
the glob bar. It is NOT a required check, because LedgerxFactory has no CI —
and this change does not claim one. The claim is precisely: *a human-run bar
that anyone can run, that fails loudly, and whose absence from CI is recorded as
a successor.*

**A FOURTH and FIFTH declaration exist and are deliberately NOT in the
invariant.** openxFactory's own `contracts/openxwallet-pin.yaml` and its nested
`openXwallet` gitlink pin the same product for openxFactory's own consumption;
the aggregation's root gitlink will be a sixth when P4 lands. Those are
governed by `neutral-product-pin`, whose requirement is that the AGGREGATION
ROOT equals openxFactory's NESTED gitlink — a rule about openxFactory's
consumption, not about a domain descendant's. LedgerxWallet and openxFactory are
INDEPENDENT CONSUMERS of one product and may legitimately pin different commits.
Agreement today (`63f5a1ad…` in all of them) is the STARTING STATE, not an
invariant, and after this change the commit governing the Ledgerx estate is the
one LedgerxWallet pins. **Divergence is therefore not an error and is not
checked** — that is the honest statement, and it replaces a weaker earlier one
("a divergence is REPORTED") which named no reporter.

### D8 — `profile/custody-posture.yaml` is new, and says so

**Decision.** LedgerxWallet declares the Ledgerx wallet custody posture as a
profile artifact: `custody.model: holder_readable`, environment-evidencing,
authority ceiling `act`, and the audit-record rule that a signature evidences the
ENVIRONMENT and the record says "environment", never "holder".

**It is a NEW ARTIFACT, not a relocation, and the packet does not launder it.**
That posture exists today only in YAML comments inside the two wallet records and
in the ratification prose of
`modify-ledgerx-posting-authority-for-segregation-of-duties` (Brett Heap,
2026-08-08, "custody stays environment-evidencing for now"). There is no custody
artifact in LedgerxFactory: `policies/` holds eight files and `docs/`
twenty-one, and none of either is wallet custody.

Authoring it here is permitted — it is profile, not fork — and is worth doing in
the same act that creates the profile's home, because a posture that lives only
in comments cannot be validated and cannot be inherited by a second tenant. But
it is scope this change ADDS rather than MOVES, so it is separable: **cutting it
to a successor costs nothing else in this packet**, and the bench should be able
to cut it in one line. The custody FACTS stay in the tenant records
(`custody.model` per wallet); the posture declares what those facts are allowed
to be, and the validator checks the records against it — which is the same
profile/instance relationship as everywhere else here, not a second truth.

### D9 — The relocation and a prepared live window: repoint in the same commit

**Decision.** `specs/016-posting-segregation-of-duties/runsheet.md:23` and
`quickstart.md:15` are repointed IN THE SAME COMMIT as the `git mv`, and the
window's operator is told. The window is NOT waited on.

`runsheet.md` carries `Status: prepared (this feature performs NONE of it)` and
reaches the relocating template by a RELATIVE LINK,
`[templates/wallet-exercise.template.yaml](../../templates/wallet-exercise.template.yaml)`.
Its phases 1–6 have not run; the ratified change that owns it,
`modify-ledgerx-posting-authority-for-segregation-of-duties`, is still ACTIVE and
archives on that window's step 6.3. So this is the one place where a topology
change can break something about to be PERFORMED — with a real operator, an
ADMIN, an OPSX lane and key minting — rather than something merely read.

*Rejected: waiting for the window to close.* It parks P6 behind precondition P0.4,
a decision this change does not own and cannot forecast.
*Rejected: leaving the links to dangle and fixing them later.* A prepared
procedure with a dead link is a broken procedure, and "later" has no owner.

The repoint is a LINK change only. No step, actor, abort condition or evidence
requirement is touched — the runsheet is an operational record and this change
edits exactly the two references whose targets it moved.

### D10 — A `git mv`, not a carve; provenance in prose

**Decision.** The three files are moved by `git mv` across a repository boundary
into a repository created EMPTY. There is no `git filter-repo`, no history
import, and no byte-identity floor.

The parent's P2 needed all three because eight openxFactory-REGISTERED artifacts
and two PROMOTED capabilities were leaving a governed corpus, where a diff that
is not provably empty cannot be bisected. Nothing of that kind moves here: the
three paths are LedgerxFactory-authored, carry no openxFactory manifest row,
appear in no `contracts/releases/*.digests.yaml`, and — verified — carry NO digest
row in `models/protected-surface.yaml` (its single wallet mention, `:438`, is
prose inside a `stack.yaml` pin entry).

The obligation that DOES fall out is different and is discharged as a task:
**a fresh-repo scaffold loses `git log`**, so LedgerxWallet's `README.md` records
the origin repository, the authoring change
(`modify-ledgerx-posting-authority-for-segregation-of-duties`, ratified
2026-08-08), the Speckit features that amended each file (016, 017, 019), and the
LedgerxFactory commit each file was taken from. Provenance in prose is weaker
than provenance in history; naming it as weaker is the point.

## Risks and trade-offs

- **Two seams where there was one.** The validator and its scan target now live
  in different repositories, and so do the profile and the estate it constrains.
  Paid for by D5's declared estate root and D4's delegating entry, both of which
  are code rather than convention. The alternative — move everything — buys one
  repository and makes the second Ledgerx tenant a fork question.
- **Nested-only means outside every governed-repo enumeration** (D2). Accepted
  because the descendant carries no ideation corpus; revisited if it ever does.
  The same condition has been true of `MedxAvatar` for five months.
- **The invariant is enforced by a human-run bar, not by CI.** D7 states this
  rather than implying a check. If nobody runs the bar, nothing catches a
  three-way disagreement. Recorded as the packet's most honest weakness and as a
  named successor.
- **`profile/custody-posture.yaml` is added scope** (D8), separable in one line.
- **A prepared live window is edited** (D9). The edit is two links and no steps,
  but it is an edit to an operational procedure with a real operator, and the
  operator must be told rather than discovering it.
- **First-of-a-standard risk.** No descendant has previously been created under
  `domain-descendant-boundary`; DTN-022's `MedxAvatar` predates it, and
  `MedxChart`'s establishing act is `draft`. Whatever this packet gets wrong
  becomes the shape three more domains copy — which is the argument for the
  decidable test in D3 rather than a list of three files.

## Migration plan

Realization is SPECKIT features, one per `tasks.md` group, in this order — per
the convener's standing correction that OpenSpec ratifies the boundary and
Speckit builds it.

1. **`[OPERATOR]`** Create `opensoft/LedgerxWallet` (private, empty). Create its
   ruleset in EVALUATE mode.
2. Scaffold LedgerxWallet: `README.md` (with D10's provenance block),
   `CLAUDE.md`/`AGENTS.md`, `.github/CODEOWNERS`. Add the nested `openXwallet`
   gitlink at `wallet-v1.1^{commit}` AND `contracts/openxwallet-pin.yaml` in ONE
   commit (D1).
3. Move the profile in (D3): the exercise template, the DHC under
   `profile/distinct-holder-constraints/`, the validator with D5's single
   candidate and declared estate root and D6's expected-set read. Add
   `profile/custody-posture.yaml` (D8).
4. **`[LedgerxFactory]`** In ONE commit: nest the `LedgerxWallet` gitlink and
   `.gitmodules` entry; delete the three moved paths; write the delegating bar
   entry (D4); write the estate manifest (D6); re-source `stack.yaml`'s
   `contract_source` (D7); amend the allowed-kind registration in
   `tests/validate_document_estate_surface.py`; repoint `runsheet.md:23` and
   `quickstart.md:15` (D9); update `README.md`, `.github/CODEOWNERS` and
   `models/protected-surface.yaml`'s prose reference.
5. Evidence: the bar green (all `tests/validate_*.py` by exit code, with the
   wallet estate reached through the delegator); the three-way pin agreement
   printed; a proof that the delegator refuses with the remediation string on an
   uninitialized submodule; a proof that the moved validator refuses on an estate
   root with no `tenants/*/wallets/`.
6. **`[OPERATOR]`** Promote the LedgerxWallet ruleset to ACTIVE once its first
   check has reported; tag `lxw-v1.0`.
7. **`[openxFactory]`** This packet's own bookkeeping: the README Records entry,
   and DTN-026's status line noting the first descendant exists.

**Rollback** is a reverse `git mv` plus restoring the two LedgerxFactory gitlink
and `stack.yaml` lines. No upstream history is rewritten and no openXwallet
content is touched, so rollback is a revert rather than a recovery.

## Open questions

**Q2 (carried from the parent) — do `tenants/ledgerxcorp/wallets/*` move into
LedgerxWallet, or stay as tenant data?** Recommended: **STAY**, on D3's test —
they would not be identical for a second Ledgerx tenant. The profile
(template, constraint set, validator, custody posture) moves; the estate stays.
The cost of the recommendation is the two seams named under Risks, and it is
recommended anyway because the alternative makes the second tenant a fork
question.

This is the one question this packet carries. Everything else above is a decision
it takes and defends.
