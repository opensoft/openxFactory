# Alignment review — stack architect

Lens: LAYER CORRECTNESS and RULE CONFORMANCE. Measured against
`split-openxwallet-repo`'s ratified `domain-descendant-boundary` (five
requirements) and its sibling `neutral-product-pin`, read at `openxFactory
origin/main`. LedgerxFactory read at `origin/main` AFTER P5b (`b131286`, work
commit `1a8ec62`, feature `019-openxwallet-consumer-repoints`).

**Draft reviewed:** `90f7ed2c` ("P6: the wallet-kind enumeration is complete and
checkable"), i.e. `proposal.md` + `.openspec.yaml` + `spec.md` + `design.md` +
`tasks.md`. An earlier pass of this review was written against `08ca4532` and has
been re-cut; where `4255b206`/`90f7ed2c` fixed a finding, that is recorded rather
than dropped, because the fixes are the strongest evidence the packet is being
authored honestly.

**Headline:** This packet now instantiates the five ratified descendant rules
correctly, and on the two questions a reviewer would expect it to fumble — the
pin-skew set and the "reported by what?" problem — it is RIGHT, explicitly and
in its own words. D7 enumerates the fourth, fifth and sixth declarations of the
openXwallet commit, scopes `neutral-product-pin`'s root-equals-nested rule as a
statement about openxFactory's consumption rather than a descendant's, and
replaces an earlier "a divergence is REPORTED" with "divergence is therefore not
an error and is not checked"; D5 enumerates the moved validator's cross-repo
location dependencies instead of assuming one. What remains wrong is narrower and
sharper than before, and two items are hard mechanical breaks rather than
opinions. **First:** `tasks.md` 5.5 edits `stack.yaml` while 5.9 asserts "no
digest re-pin is owed" — but `models/protected-surface.yaml:384-385` PINS
`stack.yaml` by digest, and the same entry at `:442-445` records the seventeen
days this repository spent red the last time that step was skipped. **Second:**
D5's location-dependency enumeration is declared complete ("enumerating them is
what makes D5 sufficient rather than plausible") and omits the one leg that the
DHC relocation actually breaks — `check_real_estate()` passes `REPO` to the
pinned openXwallet validator as its REPO-SCAN target and asserts `>= 5`
wallet-family artifacts (`:721`, `:725-729`); moving the constraint out of
`tenants/ledgerxcorp/wallets/` takes that count from exactly 5 to exactly 4, by
the packet's own arithmetic at `proposal.md:193-203`. Everything else is
citation hygiene, one false claim about the template, one over-reach in spec
requirement 5, and a set of gaps the packet has already started naming.

---

## Per-requirement conformance — the five ratified rules

| # | Ratified requirement (`domain-descendant-boundary`) | Verdict | One line |
| --- | --- | --- | --- |
| R-1 | A domain consumes a neutral product through a descendant repository (`spec.md:5-27`) | **SATISFIED** | D5 DELETES the walk and the candidate tuple rather than narrowing them ("after this change there is nothing to break a tie between"); scenarios 1-3 all met, and scenario 2's openxFactory carve-out is correctly invoked to leave openxFactory's own pin alone. |
| R-2 | A descendant pins the product by commit, twice (`spec.md:29-52`) | **SATISFIED as declared; scenarios 1-2 wired in the WRONG repository** | Pin file, kind form, `relationship:` and the same-commit rule are all declared, and scenario 3 (no retro-fit of `MedxAvatar`) is handled cleanly by D1. But the ratified text says "the DESCENDANT'S OWN validator REFUSES the tree", and `tasks.md` 5.4 puts the only refusal in LedgerxFactory's delegator. See F6, F9. |
| R-3 | A descendant carries profile, never fork (`spec.md:54-73`) | **SATISFIED (no fork), with two caveats** | Nothing forked, nothing vendored, and scenario 3's permission for a domain validator is correctly cited. Caveat one: the moved template is not tenant-free and the packet's own req-3 scenario refuses it (F3). Caveat two: scenario 2's stated detector is "the pin's DIGESTS"; the pin carries none and the spec substitutes the commit — a defensible substitution D1 now argues for, but the substitution should be named (F20). |
| R-4 | A descendant is placed at a ratified placement (`spec.md:75-100`) | **SATISFIED — exemplary** | Takes the RATIFIED nested placement, states the other's REALIZED-not-ratified standing rather than blending it, declines it with a real criterion, carries the both-placements same-commit rule forward, AND now prices the decision (D2, "the governance-visibility price it pays"). All four scenarios addressed. |
| R-5 | A descendant is created on its first profile, not before (`spec.md:102-119`) | **SATISFIED, with one over-reach** | The gate is met on verified artifacts and the packet argues for exactly one repository. The over-reach is that its own requirement 5 re-legislates the rule for four sibling domains rather than citing it (F8). |

`neutral-product-pin`'s "The consuming repository's pin is authoritative among
reachable checkouts" (`spec.md:57-77`): the third reachable checkout at
`LedgerxFactory/LedgerxWallet/openXwallet` **falls outside** that rule — it
neither breaks nor widens it, because the rule binds the aggregation-root ↔
openxFactory-nested pair only. **The packet reaches exactly this conclusion**
(`design.md` D7, "a rule about openxFactory's consumption, not about a domain
descendant's"), and it is correct.

---

## Findings

### F1 [MISMATCH] `stack.yaml` is a pinned file, and two tasks now assert the opposite

**EVIDENCE.** `tasks.md:191-195` (5.5) edits `stack.yaml`'s
`openxwallet.contract_source` and its derivation comment, and says nothing about
a digest. `tasks.md:215-216` (5.9) then closes the question in the wrong
direction:

```
      at `:438` — a pointer amendment only. Verified: that file carries NO digest
      row for any of the three moved paths, so no digest re-pin is owed.
```

The premise is true and the conclusion does not follow. `stack.yaml` is not one
of the three moved paths; it is a fourth file this change edits, and
`models/protected-surface.yaml:384-385` reads:

```
  - path: stack.yaml
    digest: "5f589a7d095aedba85f41ad07d16158b665090e21cbe6a8147280eba39a4b8bc"
```

`docs/protected-surface.md:66-70`: "edit it, recompute its digest, and update the
entry with the reason recorded beside it. An unattributed re-pin defeats the
point of pinning." P5b did exactly that — `models/protected-surface.yaml:387-388`,
"Re-pinned 2026-08-27 (second bump that day) IN THE SAME COMMIT as the change
that modified the file" — and the same entry records the cost of skipping it, at
`:442-445`: "The unpinned window showed as `[baseline] stack.yaml diverges from
its pinned digest` in `validate_onboarding_contracts.py`, red on main for
seventeen days."

Same correction in `proposal.md:398-403` and `design.md:397-398`, which carry the
identical inference.

**REMEDY.** Fold the re-pin into 5.5, not 5.9: recompute `sha256sum stack.yaml`,
update `models/protected-surface.yaml:385`, and write the reason at `:386` naming
this change — in the same commit as the `contract_source` edit. Gate it in § 6
on `python3 tests/validate_onboarding_contracts.py`. Then 5.9's sentence becomes
true as written: no digest re-pin is owed *for the three moved paths*.

### F2 [MISMATCH] D5's location-dependency enumeration is declared complete and omits the leg the move breaks

**EVIDENCE.** `design.md` D5 enumerates THREE jobs for the declared estate root —
the estate scan, `REPO/stack.yaml`, and `find_aggregation()`'s second walk — and
stakes the decision's sufficiency on that enumeration being exhaustive
("enumerating them is what makes D5 sufficient rather than plausible"). It is not
exhaustive. `tests/validate_wallet_estate.py` uses `REPO` in five places, and two
are unlisted:

```
721	    proc = run_validator(REPO, strict=True)
…
725	    m = re.search(r"repo scan: (\d+) openxWallet artifact", proc.stdout)
726	    if not m:
727	        err("upstream validator output carried no repo-scan count")
728	    elif int(m.group(1)) < 5:
729	        err(f"expected >=5 wallet-family records validated, saw {m.group(1)}")
```

and the constraint load, which reads `WALLET_DIR` alone (`:735-746`) and is
checked at `:774-776`:

```
    dhc = constraints.get(EXPECTED_CONSTRAINT)
    if dhc is None:
        err(f"missing distinct-holder constraint {EXPECTED_CONSTRAINT}")
```

**The arithmetic is the packet's own.** `proposal.md:193-203` establishes that
LedgerxFactory `origin/main` holds exactly seven wallet-kind files, of which five
carry `xfactory_wallet_*` kinds the upstream scan counts: two
`xfactory_wallet_record`, two `xfactory_wallet_grant`, one
`xfactory_wallet_distinct_holder_constraint`. Relocate the constraint and the
count is 4. `elif int(m.group(1)) < 5` then reds the bar on the very run § 6.2
holds up as evidence.

D6 does handle `EXPECTED_CONSTRAINT` ("travels, because after § D3 the constraint
IS a profile artifact"), which is the right call — but it does not follow through
to the two mechanical consequences: the constraint must now be loaded from the
PROFILE root while records load from the ESTATE root, and the artifact floor is
now a per-root number.

**REMEDY.** Make D5's list FIVE jobs. Add: (4) the pinned validator's repo-scan
target and its `>= 5` floor, restated as two floors — the estate root's
`xfactory_wallet_*` count (4 after the move) and the profile root's (1, the
constraint) — with the reason the number changed recorded beside it, exactly as
`:725-729`'s comment history does; and (5) the constraint load, from the profile
root. Add a § 6 RED proof that a wrong floor is caught, since a floor that
silently tracks whatever is present is not a floor.

### F3 [MISMATCH] The moved template is not tenant-free, and the packet's own req-3 scenario refuses it

**EVIDENCE.** `proposal.md:163` and now also `design.md:156` ("Yes — a stub
naming no tenant") justify the template as naming no tenant.
`templates/wallet-exercise.template.yaml` names one throughout:

- `:24` `grant_ref: "<grant-lx-create-01 | grant-lx-post-01 | the rehearsal grant>"`
- `:34` `presenting_key_ref: "<key-lx-creator-01 | key-lx-poster-01 — REQUIRED when verified>"`
- `:38` `wallet_ref: "<wal-lx-creator-01 | wal-lx-poster-01>"`
- `:39` `holder_ref: "<agent:lx-ap-intake-creator | agent:lx-posting-agent>"`
- `:48` `constraint_ref: dhc-lx-create-post-01`
- `:4` "land beside the estate evidence under `tenants/ledgerxcorp/ledger-estates/`"

By the packet's own discriminator — the DHC qualifies as profile because "It names
no tenant, no wallet and no key" (`proposal.md:164`) — the template fails on all
three. And its own `spec.md:92-94` refuses from the descendant "a wallet record,
capability grant or exercise record carrying a tenant's holder id, DID or key
id". The template carries holder ids and key ids.

The template still BELONGS in the descendant; the reason given is wrong. Its real
qualification is the one the same table row already states: it declares the
DOMAIN RULE SET (presenting-key requirement, `custody_model_in_force` reading,
`unattributed` for an unestablishable key, BC transport as transport) — which is
interpretation, not instance data. That argument survives the ids; "naming no
tenant" does not.

**REMEDY.** Delete the "naming no tenant" clause from `proposal.md:163` and
`design.md:156` and let the rule-set argument carry the row alone. Then narrow
`spec.md:92-94` to RECORDS so a template enumerating its domain's live ids as
placeholder guidance is not caught by the descendant's own admission rule.
Alternatively generalize the placeholders — but that needs
`proposal.md:447-449`'s "Out of scope" list amended to admit a fourth mechanical
change, and it makes the template less useful to the window's operator.

### F4 [DRIFT] Three stale line citations, two of them now hardened into tasks

**EVIDENCE.**

1. `models/protected-surface.yaml` — the sole `validate_wallet_estate.py` mention
   is at **`:455`**, not `:438`, in a 781-line file; P5a.2 and P5b inserted the
   `openxwallet:` pin narrative above it. Cited as `:438` at
   `proposal.md:111` and `:400`, `design.md:398`, and `tasks.md:215`.
2. `specs/016/quickstart.md` — `:15` is the opening ```` ```sh ```` fence. The
   relative validator invocation is at **`:19`**
   (`python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`),
   and a SECOND stale surface sits at `:3-7`: "the pinned openxFactory checkout
   at the workspace root, with its nested `openXwallet` gitlink initialized" — a
   prerequisite that becomes false at P6 and that the repoint does not name.
   Cited as `:15` at `proposal.md:221`, `design.md:366` and `tasks.md:199`.
3. `design.md` D5 job (1) cites the estate-directory `err()` at `:706`. On
   `origin/main` it is at **`:733`** (`:732` is
   `if not os.path.isdir(WALLET_DIR):`). D5's other two citations — `:583-594`
   for `find_aggregation()`'s walk body and `:688` for the `git show` — are
   exact.

**REMEDY.** Re-cite all three against `origin/main`, and extend task 5.6 to
`quickstart.md:3-7` as well as `:19`. A packet whose thesis is "one commit, three
declarations, no drift" cannot ship stale line numbers in its own task list; and
5.6 is a task an implementer will execute literally.

### F5 [DRIFT] A second amendment site in the file task 5.8 already opens

**EVIDENCE.** `tasks.md:207-211` (5.8) amends ONE registration in
`tests/validate_document_estate_surface.py` — `ledgerx_wallet_exercise_template`,
whose CHK002 note is at `:1116-1121`. The same file, forty lines earlier at
`:1094-1098`, says:

```
    # and the validator runs from openxFactory's nested gitlink
    # (openxFactory/openXwallet/scripts/validate-openxwallet.py) — see
    # find_openxfactory() in tests/validate_wallet_estate.py for the
    # ordered candidates. Corrected at P5b: ratified split-openxwallet-repo
    # tasks.md 10.6, feature 019-openxwallet-consumer-repoints.
```

Both sentences become false at P6 — the validator will run from LedgerxWallet's
nested gitlink, and `find_openxfactory()` will not be in that file or that
repository. `:1097`'s own "Corrected at P5b" proves this is a maintained,
load-bearing prose surface rather than dead comment.

For completeness, the full path-reference sweep of LedgerxFactory `origin/main`
for the three moved paths returns nine sites: `README.md:109`;
`specs/016/negative-confirmations.md:43`; `specs/016/runsheet.md:23`;
`specs/016/tasks.md:77,91,127,215`;
`tests/validate_document_estate_surface.py:1096,1120`. Plus
`models/protected-surface.yaml:455` and `specs/016/quickstart.md:3-7,19`. Task
5.8/5.9 covers all but `:1096` and the quickstart prerequisite.

**REMEDY.** Add `:1086-1098` to task 5.8.

### F6 [GAP] The pin refusal is wired in the consumer, not in the descendant

**EVIDENCE.** `domain-descendant-boundary:42-48` puts the refusal inside the
descendant: "the DESCENDANT'S OWN VALIDATOR REFUSES the tree rather than
preferring either", and "a commit changes the gitlink without changing the pin
manifest … the change is refused". The packet restates both (`spec.md:28-34`) and
then wires them at `tasks.md:182-190` (5.4) into LedgerxFactory's delegating
entry, which "read[s] and compare[s] the THREE pin declarations (D7) and refuse[s]
on disagreement". D7 confirms: "The delegating bar entry (§ D4) reads all three".

The consequence is asymmetric in a way the ratified rule cares about. Clone
LedgerxWallet on its own — which is the mode its own branch-protection ruleset
and `lxw-v1.0` tag exist for — and a gitlink moved without its pin manifest is
caught by nothing. The two-declaration same-commit rule is the descendant's
INTERNAL invariant; only the third declaration is the consumer's.

**REMEDY.** Split the check. Put a two-declaration check in LedgerxWallet
(`tests/validate_pin.py`: `git ls-tree HEAD openXwallet` equals
`contracts/openxwallet-pin.yaml`'s `revision`; `revision` is 40 hex; no bare tag
stands in for it; fail closed with the `git submodule update --init openXwallet`
remediation string), make it the check task 6.1 waits on before promoting the
ruleset to ACTIVE, and leave the THIRD declaration where it belongs — in
LedgerxFactory's delegator, which is the only place `stack.yaml` is readable.
That also gives `spec.md:28-34` a home in the repository its subject is.

### F7 [DRIFT] The estate-root default is placement-dependent under a rule the packet itself carries forward

**EVIDENCE.** `design.md` D5: "an explicit parameter, defaulting to the parent
directory of the LedgerxWallet checkout" — and later, correctly, "it is not
optional. A default is a convenience for the nested layout". The ratified rule
the packet cites at `spec.md:55-57` permits BOTH placements
(`domain-descendant-boundary:98-100`), and in the `xFactories/LedgerxWallet`
placement the parent directory is `xFactories/`, which has no
`tenants/*/wallets/`, no `stack.yaml`, and an aggregation root immediately above
it. Two of D5's three refusals fire, and the third resolves — so the default is
correct in exactly one of the two ratified placements and confusing in the other.
The corpus also legislates against defaulting a scan target at all:
`neutral-product-pin:100-106`, "a self-test that opens no governed surface is a
green check that verified nothing."

**REMEDY.** Drop the default. D5 already argues the parameter is not optional;
finish the argument — refuse when the estate root is not passed, with a named
exit. The delegator passes it (5.4 already does), so nothing relies on the
default except a bare invocation, which is exactly the case that should refuse.

### F8 [MISMATCH] Spec requirement 5 re-legislates ratified neutral law for four other domains

**EVIDENCE.** `spec.md:151-159`: "the sibling descendants `MedxWallet`,
`codexWallet`, `OpsxWallet` and `AdxWallet` SHALL NOT be created until their own
domain tree carries at least one wallet profile artifact". The ratified rule
already binds this generally at `domain-descendant-boundary:102-107`, and
`proposal.md:361-369` says this change "issues no delta against them" and "does
not amend them". A domain-scoped capability carrying a SHALL over four other
domains creates two sources for one obligation, and the restatement will not move
if the neutral rule is ever amended — which is the failure mode
`document-lifecycle`'s explicit-delta rule exists to prevent, and which the
parent's own Amendment 2 was authored to avoid.

Same class, milder: `spec.md:55-57` and `:72-74` restate ratified rule 4's
placement scenarios, and `spec.md:139-141` reproduces `neutral-product-pin:53-55`
nearly word for word.

**REMEDY.** Scope requirement 5 to LedgerxWallet's own creation gate and cite the
ratified rule for the siblings: "the sibling names are registered under R7; their
creation gate is `domain-descendant-boundary`'s, not this capability's." Trim the
restated placement and remediation scenarios to citations.

### F9 [DRIFT] The pin shape diverges from the live example D1 says it follows

**EVIDENCE.** `proposal.md:136-139` and D1 both take the shape from
`MedxChart/contracts/openchart-pin.yaml`. That file nests six fields under a
`pin:` mapping (`:4-10`):

```
pin:
  repository: opensoft/openChart
  remote: git@github.com:opensoft/openChart.git
  revision: d2376a31dbafa413d8e5ba032f4a2620a75d578e
  submodule_path: openChart
  source_path: .
  relationship: pinned_upstream_composition
```

The packet declares its fields FLAT, drops `remote` and `source_path`, and adds
`revision_kind` and `contract_bundle_tag` — four of six overlap and the mapping
shape differs. "The same six pin fields" (`proposal.md:138`) is not what follows,
and the difference is load-bearing: a check reading `pin.revision` finds nothing
in a flat file and vice versa. This compounds F6, where the check that would have
caught it does not exist in the descendant.

**REMEDY.** State which of MedxChart's six are carried, which are dropped and
why, and whether the mapping is flat or nested. The KIND choice —
`ledgerxwallet_openxwallet_pin` on `medxchart_openchart_pin`'s compressed form
rather than `medx_avatar_openavatar_pin`'s underscored one — is defensible on a
corpus that disagrees with itself and whose ratified rule names both; keep it and
say that is why. Note in passing that it breaks from LedgerxFactory's own
`ledgerx_wallet_*` kind namespace, which is fine and worth one clause.

### F10 [DRIFT] `contract_source:` departs from a ratified design value without naming it

**EVIDENCE.** The parent's D9 (`design.md:383-392`) specifies the sibling block
"field for field", including `contract_source: openxFactory-nested-submodule-pin`,
realized as its `tasks.md` 10.2/10.3 and landed at `1a8ec62`
(`LedgerxFactory stack.yaml:59`). This packet's D7 and `tasks.md` 5.5 change it
with a correct reason and never mention that D9 named the value being replaced.

**REMEDY.** One sentence in D7: D9 is a design decision rather than a spec
requirement, so no delta against `split-openxwallet-repo` is owed — and the
substitution is what rule 1 compels once the descendant exists. Say it so the
bench does not have to derive it.

### F11 [NOTED] `profile/custody-posture.yaml` would be a declaration nothing reads

**EVIDENCE.** `tasks.md:161` (4.4) and D8 both name it NEW and separable, and
`design.md:423` offers it as cuttable "in one line" — good practice. Two reasons
to take the offer. First, nothing would read it: `proposal.md:447-449` puts
content changes to the moved files beyond the mechanical set out of scope, so the
validator keeps hard-coding the posture at
`tests/validate_wallet_estate.py:141-142`
(`ENVIRONMENT_EVIDENCING = {"holder_readable", "isolated_invocable"}`) and never
opens the new file. Second, the custody FACTS are already declared per record —
`tenants/ledgerxcorp/wallets/wal-lx-creator-01.yaml:27-31` carries
`custody.model`, `registry_version`, `declared_at`, `declared_by` — so a
repo-level posture beside per-record custody is a second declaration of one fact
with no reconciliation rule, which is the "two answers to one question" the
packet refuses for pins.

Filing note: under LedgerxFactory's own rules an ENFORCED posture belongs in the
protected `policies/` directory (`models/protected-surface.yaml:46-55`;
`docs/protected-surface.md:50-56`, "`policies/` holds policy this domain
*enforces*"). Authoring it into an unprotected `profile/` tree moves an enforced
statement out from under digest protection.

**RECOMMENDATION.** Cut to a successor and let that successor decide reader and
home together. The verified survey behind it (`policies/` holds exactly eight
files, `docs/` twenty-one, none of them wallet custody) is the right groundwork
and should travel with the successor.

### F12 [NOTED] `code_surface` names a repository it says is untouched, and omits the one it edits

**EVIDENCE.** `proposal.md:2` declares "THREE repositories: a NEW repository, one
consumer, and the aggregation's placement record", then in the same field: "(3)
The xFactory aggregation: NO change in v1 … `.gitmodules` at the aggregation is
untouched". openxFactory — which receives this packet plus a README "OpenSpec
Records" row (`proposal.md:3`, `:421-423`) — is not among the three.

**REMEDY.** `code_surface: opensoft/LedgerxWallet (new), LedgerxFactory,
openxFactory (this packet plus one README Records row)`. Keep the aggregation
statement, in § 6, where it is a decision rather than a surface.

### F13 [GAP] The prepared live window gains a repointed link and a verbal notice, but no precondition

**EVIDENCE.** `tasks.md:196-204` (5.6) repoints the two references in the same
commit and is explicit that it touches "LINKS ONLY: no step, actor, abort
condition or evidence requirement"; `:205-206` (5.7) makes telling the operator
its own task. Both are right. What is missing is the durable form: after the
move the operator cannot READ the template without initializing the submodule,
and `specs/016/runsheet.md`'s Phase 0 (`:27-61`) — P0.1-P0.3 SATISFIED, P0.4 open
("the gate stays because Brett has not chosen a branch", `:60`) — says nothing
about it. A verbal notice does not survive into the tree the operator reads
weeks later.

**JUDGEMENT — the packet is right on the contested question.** A same-commit
repoint of a PREPARED procedure IS sound here: the window is not in progress, the
repoint alters no step, and waiting on P0.4 would park P6 behind a decision it
does not own. `README.md:117-119` corroborates the state exactly as quoted.

**REMEDY.** Add a P0.5 to the runsheet in the same commit, naming
`git submodule update --init LedgerxWallet` — the same remediation string 5.4
promises the delegator will print. Then 5.7's notice has something to point at.

### F14 [GAP] `neutral-product-pin`'s human-only floor: half-met, and the half that is met is not claimed

**EVIDENCE.** `neutral-product-pin:120-127` — the pin file and the gitlink "SHALL
therefore be named in the consuming repository's merge-gate floor as
never-clearable paths". LedgerxFactory has no workflow and no floor (`.github/`
holds `CODEOWNERS` and `copilot-instructions.md`), and `tasks.md:87` disposes of
the topic as "P3b (codexFactory's merge-gate floor) is codexFactory's". Two
things are already right and unclaimed: `tasks.md:213` adds a `/LedgerxWallet`
line to LedgerxFactory's CODEOWNERS — an owner review over the gitlink, which
that file's current eight directories plus `/stack.yaml` (`:20-29`) do not
provide — and `tasks.md:103-105` puts `@opensoft/xfactory` over LedgerxWallet's
`/contracts/`, i.e. over its pin file. Still uncovered: LedgerxFactory's
`.gitmodules`, and any floor at all in either repository.

**REMEDY.** State that the floor clause is scoped to repositories that have a
floor, name the CODEOWNERS lines as the substitute human gate over "which reader
runs" (they are a real control and deserve the credit), add `/.gitmodules`
alongside `/LedgerxWallet`, and register the floor beside the CI successor
already named at `proposal.md:436-444`.

### F15 [NOTED] The wallet-kind enumeration is complete — verified independently

Calibration. `proposal.md:193-203`'s claim checks out: `git grep '^kind:.*wallet'`
over LedgerxFactory `origin/main` returns exactly seven files —
`templates/wallet-exercise.template.yaml` (`ledgerx_wallet_exercise_template`),
`schemas/holder-registry.schema.yaml` (`ledgerx_wallet_holder_registry_contract`),
`tenants/ledgerxcorp/wallets/dhc-lx-create-post-01.yaml`, two
`xfactory_wallet_grant` and two `xfactory_wallet_record`. A wider
case-insensitive sweep for wallet REFERENCES across `conformance/`, `catalog/`,
`profiles/`, `omnigent/`, `hermes/`, `workflows/`, `adapters/`, `models/`,
`schemas/`, `credentials/` and `policies/` adds only prose:
`omnigent/domain-overlay.yaml:11`, `openspec/specs/ledgerx-ledger-estate/spec.md:139`,
`specs/011-setup-boundary/spec.md:101,109`, and two tenant evidence files —
none of them path references, none needing amendment. **Nothing wallet-touching
is missed.** Note that `openspec/specs/ledgerx-ledger-estate/spec.md` IS a pinned
file (`models/protected-surface.yaml:252-253`), so if any reviewer proposes
touching its `:139` prose, F1's re-pin discipline applies there too.

### F16 [NOTED] D7 answers the pin-skew question correctly and completely — credit it

Calibration, and the most important thing this review has to say in the packet's
favour. The obvious attack on a three-way invariant is that the set is larger
than three. D7 pre-empts it: it names openxFactory's own pin and nested gitlink
as the fourth and fifth, the aggregation root as a sixth at P4, gets the scoping
right ("a rule about openxFactory's consumption, not about a domain descendant's"),
and then does the harder thing — replacing "a divergence is REPORTED" with
"divergence is therefore not an error and is not checked … it replaces a weaker
earlier one which named no reporter." `spec.md:68-70` was rewritten to match, and
now ends "no tool is required to reconcile them and none SHALL claim to". That is
the corpus's own LS-A3 doctrine applied by the author to the author. Verified
against the trees: `openxFactory contracts/openxwallet-pin.yaml:44`
`commit: "63f5a1ad…"`, its nested gitlink at the same commit, and the aggregation
carrying `openAvatar` at root and no `openXwallet` — the "agreement today is the
starting state" claim is exactly true.

### F17 [NOTED] Placement, and the choice to author this capability in openxFactory, are both correct

Calibration. `domain-descendant-boundary:75-84` asks that the two placements'
STANDING "be stated rather than blended". `proposal.md:300-312` with D2 states
both, takes the ratified one, names the other's draft standing (verified:
`create-medxchart-overlay-boundary` sits in openxFactory's instance at
`Status: draft`, `target_release: implementation_pending`), gives a real criterion
for declining it, prices the decision, and carries the both-placements
same-commit rule forward as a bound follow-on. It also declines to propagate
LedgerxFactory's own `[submodule "ledgerXavatar"]` / `path = LedgerxAvatar`
section-name mismatch (`.gitmodules:1-2`).

Authoring `ledgerxwallet-overlay-boundary` in openxFactory's OpenSpec instance
rather than LedgerxFactory's is likewise correct on house precedent — both
`create-medxchart-overlay-boundary` and `create-medxpractice-overlay-boundary`
live there with `specs/<name>-overlay-boundary/` deltas. And it does not breach
aggregation working rule #1 as amended by the parent's task 1.12
(`xFactory CLAUDE.md:61-64`): a Ledgerx custody posture is a domain profile
artifact and not a neutral contract, and LedgerxWallet consumes no openxFactory
version, so it owes no `stack.yaml`. Both points are worth one line each in the
packet so a reviewer does not have to derive them.

### F18 [NOTED] The delegating entry is the right construction — the alternatives were measured, not assumed

Calibration, because "is a delegator an edited copy?" is the natural challenge.
**It is not, and rule 3 does not reach it.** `domain-descendant-boundary:54-61`
forbids a fork of the NEUTRAL PRODUCT's validator;
`tests/validate_wallet_estate.py` is LedgerxFactory-authored — its header
`:1-27` cites feature 016 and the 2026-08-08 Ledgerx ratification, and
`specs/018/research.md:237` and `plan.md:248` both record it as unpinned
LedgerxFactory code. A delegator that resolves, execs and propagates an exit code
carries no rule, so it creates no second place a rule can drift; `tasks.md:189-190`
pins that explicitly ("It holds NO rule, NO threshold, NO expected set, NO probe
corpus").

The alternatives are worse, measured. Widening the glob means editing
`docs/protected-surface.md:62` plus every quickstart that repeats it
(`specs/016/quickstart.md:17`, `017/quickstart.md:20`, `018/quickstart.md:9`) and
changing the bar's contract for every future validator. A `tests/` symlink is
worse still: `os.path.abspath(__file__)` does not resolve symlinks (validator
`:38`), so `REPO` would silently resolve to LedgerxFactory — correct by accident
in the nested placement, wrong in the other — and
`shutil.copyfile(os.path.abspath(__file__))` at `:193` would copy through the
link, breaking the loud-failure probe. Keeping the validator and moving only the
template and DHC remains the smallest v1 and is worth one line in D4's rejected
alternatives, since it dissolves F2, F6 and F7 outright; but with D5 and D6 now
written, the chosen construction is defensible on its own terms.

### F19 [NOTED] The bar is red-by-construction in this workspace, so the green-evidence tasks need a named precondition

**EVIDENCE.** On `origin/main` the finder holds two candidates, both in other
repositories (`:53-78`). `/home/brett/projects/xFactory/openxFactory/openXwallet`
does not exist and the aggregation carries no root `openXwallet`, so
`find_openxfactory()` returns `None` and `main()` (`:798-803`) exits 1. Measured
live: the local openxFactory checkout sits at `26e1e021` — the exact commit the
validator's own docstring names as predating the deprecating minor (`:606-608`) —
and still carries the shed `scripts/validate-openxwallet.py` on disk (110329
bytes, 2026-08-26); the working tree's PRE-P5b copy of the validator resolves
THAT file and reports `WALLET ESTATE: PASS`. That is precisely the silent pass
P5b's inverted probe exists to catch (`:312-314`,
`("legacy-only", [(_LEGACY, 1)], None)`), observed in the wild.

**REMEDY.** Name an initialized checkout as a precondition of tasks 6.2, 6.3,
6.5 and 6.5a. And put the observation in § Why: it is the packet's strongest
concrete benefit — after P6 the estate's reader cannot be a stale sibling
checkout, because there is one candidate and its commit is declared.

### F20 [NOTED] D1 rejects the digest block; say what the Ledgerx reader gives up

**EVIDENCE.** openxFactory's pin carries eight per-file `sha256`
(`contracts/openxwallet-pin.yaml:70-86`), a `pinned_by_commit_only:` set
(`:95-101`) and `verify_pin: scripts/verify-openxwallet-pin.py` (`:64`). D1 now
addresses this and rejects a descendant digest block with a real argument
(`design.md:92-104`), which conforms: `domain-descendant-boundary:29-40` requires
only commit-twice of a descendant. The residual is that after P6 the reader
adjudicating the Ledgerx estate lives in a checkout verified by gitlink equality
alone, where today's resolution path runs through openxFactory's digest-verified
nested gitlink — and `neutral-product-pin:79-86` asks that "the pin's digests
SHALL be verified BEFORE the pinned reader is invoked". Scoped to openxFactory
and to required checks, so not a breach; still a change in effect.

**REMEDY.** One Impact bullet: the Ledgerx reader becomes gitlink-verified rather
than digest-verified; digest verification of openXwallet remains openxFactory's;
this is what the ratified descendant rule asks for. Also amend `spec.md:100-102`,
which silently swaps rule 3 scenario 2's stated detector ("the pin's DIGESTS") for
the commit — the swap is right, D1 argues it, and the spec should say it is a
substitution rather than a quotation.

---

## Verified accurate — external citations I spot-checked

- **`wallet-v1.1` is an annotated tag `021cdeef…` dereferencing to
  `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`** (`gh api
  repos/opensoft/openXwallet/git/refs/tags/wallet-v1.1`, then the tag object).
  The instruction to resolve `wallet-v1.1^{commit}` and never the bare tag is
  right, and the annotated-tag sha in the proposal is right.
- **openxFactory's two declarations agree at that commit**:
  `contracts/openxwallet-pin.yaml:44` and
  `git ls-tree origin/main openXwallet` → `160000 commit 63f5a1ad…`.
- **P5b is merged as described**: `b131286` (PR #30), work commit `1a8ec62`
  "P5b: the dead finder candidate goes, and the wallet pin becomes a declaration".
- **`stack.yaml:51-62`** is the `openxwallet:` block; `contract_ref` at `:55`,
  `contract_source: openxFactory-nested-submodule-pin` at `:59`. Citation exact.
- **Finder citations exact**: `VALIDATOR_CANDIDATES` `:53-78`,
  `find_openxfactory()` `:81-116` with the walk at `:109-116`, `VALIDATOR =
  find_openxfactory()` `:119`; the file is 822 lines. Two candidates remain and
  both are in other repositories; the third's removal note (`:67-77`) is as
  emphatic as quoted.
- **The aggregation pins `openAvatar` at root and no `openXwallet`** — P4 is
  unlanded (58-line `.gitmodules`).
- **`opensoft/LedgerxWallet` does not resolve** (`gh repo view` → "Could not
  resolve to a Repository"); **`opensoft/LedgerxAvatar` exists** and is PRIVATE,
  so the nesting precedent is live in this domain's own tree.
- **`openspec/specs/` holds 52 capabilities**, and neither
  `domain-descendant-boundary` nor `neutral-product-pin` is among them.
- **No digest row for any of the three moved paths**, and `templates/`, `tests/`
  and `tenants/` are not protected directories — `protected_directories` is
  exactly `credentials`, `adapters`, `policies`, `openspec/specs`, `conformance`
  (`models/protected-surface.yaml:29-78`). The claim is true; F1 is about a
  fourth file.
- **`docs/protected-surface.md:62`** is the human-run glob, verbatim as quoted;
  **LedgerxFactory has no GitHub Actions workflow**.
- **`policies/` holds exactly eight files, `docs/` twenty-one**, and no wallet
  custody artifact exists in either.
- **The runsheet is `Status: prepared`** with P0.4 open; `:23` is the template
  link and `:174` names the DHC by id, so that reference does survive the move.
  **README:117-119** quoted correctly.
- **The parent's § Successors (`:1195-1197`), `tasks.md` 12.1, and Q2
  (`:1156-1162`)** match the `.openspec.yaml` quotations word for word.
- **`target_release: implemented` is a declared value** of `release-realization`
  (`openspec/specs/release-realization/spec.md:9`) and is what the parent uses.
- **`MedxAvatar/pins/openavatar.yaml`** does carry `source_repo`/`resolved_ref`
  (`:7-9`), no `relationship:`, and lives at `pins/` — D1's reason for not
  following it is correct.
- **`OPENSPEC_TELEMETRY=0 openspec validate create-ledgerxwallet-overlay-boundary
  --strict`** → "is valid"; all five requirements carry SHALL on the first line
  of the body, so the first-line parser rule is satisfied.
- **The governance-visibility gap D2 concedes is real and worse than stated in
  one respect**: `sync-notebooklm-books.py:652-653` keys on
  `^\s*path\s*=\s*(xFactories/\S+)\s*$` against the AGGREGATION's `.gitmodules`,
  `:761` builds the walk set from it, and `:629-641` `in_nested_checkout()`
  actively EXCLUDES any file under a nested `.git` (`:767`), so a nested
  descendant is skipped even inside its parent's own walk;
  `doc_health/ideation_routing.py:225-235` admits only `openxFactory` and
  `xFactories/<Name>`, and `:238-256` reports anything else as an unresolvable
  repository id. The aggregation `.gitmodules` carries neither `MedxAvatar` nor
  `LedgerxAvatar`, so D2's "exactly as `MedxAvatar` has been for five months" is
  exact. The one thing D2 does not mention: beyond projection and ideation
  routing, a STRUCTURED REFERENCE naming a nested descendant is unresolvable
  (`_repository_unknown_reason`), so no governed document can cite LedgerxWallet
  by repository id at all. Worth one clause in D2.

---

## Blocking before circulation

1. **F1** — `stack.yaml`'s digest re-pin, folded into task 5.5. Two tasks and two
   prose sections currently tell the bench that no re-pin is owed, and the
   failure mode is documented inside the very file they cite.
2. **F2** — D5's enumeration extended to the repo-scan target and its `>= 5`
   floor, and to the constraint load. The count goes 5 → 4 on the packet's own
   arithmetic, so task 6.2's green run reds as written.
3. **F3** — the "naming no tenant" claim about the template deleted from
   `proposal.md:163` and `design.md:156`; the rule-set argument carries the row
   without it.
4. **F4** — `:438` → `:455`, `quickstart.md:15` → `:19` plus `:3-7`, and D5's
   `:706` → `:733`. Task 5.6 and 5.9 will be executed literally.

## Blocking before ratification

5. **F6** — a two-declaration pin check inside LedgerxWallet, gating task 6.1's
   ruleset promotion; the three-way check stays in the delegator.
6. **F5** — `tests/validate_document_estate_surface.py:1086-1098` added to task
   5.8.
7. **F7** — the estate-root default dropped, finishing D5's own "not optional"
   argument.
8. **F8** — spec requirement 5 scoped to Ledgerx, the sibling gate returned to
   the ratified rule; the three restated scenarios trimmed to citations.
9. **F9 / F10 / F20** — the pin's field set stated against MedxChart's six;
   D9's replaced `contract_source` value named; one Impact bullet on
   gitlink-verified versus digest-verified.
10. **F11 / F13 / F14** — the custody posture cut to a successor or given a
    reader; a P0.5 precondition written into the runsheet rather than delivered
    verbally; the CODEOWNERS substitute gate claimed and `.gitmodules` added.
11. **F12 / F19** — `code_surface` corrected; an initialized checkout named as a
    precondition of every green-evidence task.
