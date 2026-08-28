# Council — Adversary Engineer

**Verdict:** RESTRUCTURE

The packet's construction contains two independently fatal defects that no
amount of prose repair reaches: (1) the moved validator **cannot go green under
its own declared task list** — the distinct-holder constraint leaves the exact
directory the validator looks in, and the `>= 5` repo-scan floor becomes 4
because openXwallet `wallet-v1.1` prunes nested repositories, both facts written
down in P5b's own merged evidence one day before this packet was authored; and
(2) the pin is a **declaration with no verifier** — nothing anywhere compares the
checked-out `openXwallet/` revision to `contracts/openxwallet-pin.yaml`, so a
fork at a different commit substitutes and every declared check still agrees.
The packet is unusually honest in its prose and its citation accuracy is high
(nine of my attacks failed against it), but §4 and §5 of `tasks.md` describe a
build that reds, and D1/D7 describe a control that does not enforce.

---

## LS-A3 findings — controls asserted, enforcement absent

> LS-A3, verbatim: "A bench must not adopt a control on a description of an
> enforcement that does not enforce it."
> — verified quoted at
> `openxFactory/openspec/changes/add-wallet-carried-review-authority/alignment-stack-architect.md:194`:
> "`lead-security.md:154-160` (LS-A3, including \"A bench must not adopt a
> control on a description of an enforcement that does not enforce it\" at
> `:158`)".

### V1 — The moved validator reds on its own terms: the DHC leaves the directory the validator reads, and the `>= 5` floor becomes 4

**IMPACT: HIGH**

**ATTACK.** `tasks.md` 4.3 declares the moved validator changes in "exactly
three mechanical changes and no rule change", and asserts `EXPECTED_CONSTRAINT`
is "BYTE-UNCHANGED". Run the bar after §4 and §5 land as written. Two
assertions fire, deterministically, in both possible wirings of the scan
target:

- `WALLET_DIR` is the estate root's `tenants/ledgerxcorp/wallets/`. Task 4.2
  moves `dhc-lx-create-post-01.yaml` OUT of that directory into
  `LedgerxWallet/profile/distinct-holder-constraints/`. The validator's DHC
  lookup reads only `WALLET_DIR`. Result: `missing distinct-holder constraint
  dhc-lx-create-post-01`.
- The repo-scan floor. openXwallet `wallet-v1.1` **prunes nested
  repositories** from the sweep, so a scan of LedgerxFactory does not descend
  into `LedgerxWallet/` (a submodule checkout carries a `.git` FILE, which the
  prune matches by design). The estate count drops from exactly 5 to 4.
  Result: `expected >=5 wallet-family records validated, saw 4`.

If instead the implementer points `run_validator` at the descendant, the count
is 1 and `WALLET_DIR` does not exist at all (`missing estate directory`). There
is no wiring of the three declared changes that goes green.

**EVIDENCE.**
- `LedgerxFactory origin/main:tests/validate_wallet_estate.py:39` —
  `WALLET_DIR = os.path.join(REPO, "tenants", "ledgerxcorp", "wallets")`
- same, `:774-776` — `dhc = constraints.get(EXPECTED_CONSTRAINT)` / `if dhc is
  None:` / `err(f"missing distinct-holder constraint {EXPECTED_CONSTRAINT}")`
- same, `:725-729` — `m = re.search(r"repo scan: (\d+) openxWallet artifact",
  proc.stdout)` … `elif int(m.group(1)) < 5:` /
  `err(f"expected >=5 wallet-family records validated, saw {m.group(1)}")`
- `openXwallet@63f5a1ad:scripts/validate-openxwallet.py:2060,2080-2081` —
  `NESTED_REPO_MARKER = ".git"` … "any directory below the scan root carrying a
  `.git` entry, **file or directory**, is a nested repository and is not
  descended into."
- **The packet's own precondition documents both dependencies.**
  `LedgerxFactory origin/main:specs/019-openxwallet-consumer-repoints/evidence/estate-run.md:104`
  — `note  repo scan: 5 openxWallet artifact(s) validated, 602 document(s)
  skipped as another kind`; and `:112` — "| `run_validator()`'s ≥5 repo-scan
  assertion unaffected by the prune | **5 artifacts validated** — the Ledgerx
  wallet records at `tenants/ledgerxcorp/wallets/` are not inside a submodule,
  so the nested-repository prune does not reach them |"; and `:120-122` — "The
  prune's own `nested repositories pruned` NOTE does not appear, and should
  not: the scanned tree contains no nested repository."

P6 falsifies both clauses of that measured statement — it puts one of the five
inside a submodule, and it makes the scanned tree contain a nested repository —
and the packet never mentions the prune, the count, or the floor. `tasks.md` 6.2
promises "The LedgerxFactory bar green".

**REQUIRED CHANGE.** Declare a FOURTH and FIFTH mechanical change on the moved
validator: (d) the DHC is read from the profile's own
`profile/distinct-holder-constraints/` rather than from `WALLET_DIR`, and (e) the
repo-scan floor is re-derived (4 for the estate tree) with the prune named as
the reason, plus a separate positive assertion that the descendant's own profile
tree was adjudicated. Record the count arithmetic (5 → 4 + 1) in `design.md`,
and cite `019/evidence/estate-run.md:112` as the source of the dependency.

---

### V2 — D5 deletes one of TWO upward walks; the survivor reads a `stack.yaml` that will not exist

**IMPACT: HIGH**

**ATTACK.** D5 states: "The five-level upward walk and the candidate tuple are
DELETED, not narrowed: after this change there is nothing to break a tie between."
The file contains **two** five-level upward walks. Task 4.3(a) deletes
`find_openxfactory()`. `find_aggregation()` survives, unnamed anywhere in the
packet, and it walks up five levels looking for a `.gitmodules` naming
`openxFactory`, then hands the resolved root to a checker extracted from
openxFactory. Its caller then does:

```python
with open(os.path.join(REPO, "stack.yaml"), encoding="utf-8") as fh:
    pin = yaml.safe_load(fh)["xfactory"]["contract_ref"]
```

After the move `REPO` is the LedgerxWallet checkout, which has no `stack.yaml`.
The bar dies with an unhandled `FileNotFoundError` inside
`check_pin_reconciliation()`, which `main()` calls **before**
`check_real_estate()` — so the estate is never validated, and the failure is a
traceback rather than a named exit with a remediation string. Either the packet
owes a fourth declared change here, or the run crashes; both contradict
`tasks.md` 4.3's "exactly three mechanical changes".

Worse for the boundary claim: with `find_aggregation()` intact, the brand-new
descendant reaches openxFactory **by directory adjacency** — the precise
resolution mechanism the §Why calls "A PATH IN SOMEBODY ELSE'S REPOSITORY,
reached by directory adjacency". The packet's own spec delta refuses this:
`specs/ledgerxwallet-overlay-boundary/spec.md:59-61` — "**WHEN** a LedgerxFactory
tool resolves the openXwallet validator at a path outside `LedgerxWallet/openXwallet/`,
such as a parent directory's `openxFactory/openXwallet/` … **THEN** the resolution
is a direct integration of the product and is refused".

**EVIDENCE.**
- `tests/validate_wallet_estate.py:583-585` — `node = REPO if start is None else
  start` / `for _ in range(5):` / `node = os.path.dirname(node)`
- same, `:132-133` — `OPENXFACTORY_DIR = "openxFactory"` /
  `PIN_CHECKER_PATH = "scripts/check-openxfactory-pin.py"`
- same, `:675-676` (quoted above), `:704-706` — `subprocess.run([sys.executable,
  checker, REPO, "--aggregation-root", aggregation], …)`
- same, `:804-809` — `check_pin_reconciliation()` is called before
  `check_real_estate()`
- `design.md:216-220` (D5's deletion claim)

**REQUIRED CHANGE.** D5 must enumerate BOTH walks. Decide explicitly whether
`check_pin_reconciliation()` (a) stays in LedgerxFactory as part of the
delegating entry — where `stack.yaml` and the aggregation walk both belong — or
(b) travels and is rewritten to take the openxFactory pin as declared input.
Option (a) is the only one consistent with rule 1; and it means the "thin
delegating entry of at most a few dozen lines" is no longer thin, which D4 must
own.

---

### V3 — The pin has no verifier: a fork of openXwallet at another commit substitutes, and every declared check still agrees

**IMPACT: HIGH**

**ATTACK.** State: LedgerxWallet checked out, submodules initialized, then

```
cd LedgerxWallet/openXwallet && git remote add f <fork> && git fetch f && git checkout f/main
```

What runs: the moved validator resolves `openXwallet/scripts/validate-openxwallet.py`
at D5's single fixed relative path and **executes the fork's copy**. The
delegator's three-way check (D7) compares the *recorded* gitlink, the pin
manifest's `revision`, and `stack.yaml`'s `contract_ref` — three declarations,
all unchanged, all agreeing. GREEN. The reader that actually ran is not the
reader the pin names, and nothing in the packet notices.

The parent closed exactly this hole and the packet discards two of its three
legs. `split-openxwallet-repo/design.md:406-410`: "**`.gitmodules` is
deliberately not added.** A URL swap alone cannot change what runs: **D2 checks
the recorded gitlink, the checked-out revision and the eight digests against the
pin**, so a fork at the same commit and bytes is inert and a fork at any other
commit fails." LedgerxWallet's pin (D1, `tasks.md` 3.4) carries no digests
(explicitly rejected), no `verify_pin:`, and no comparison of the checked-out
revision. One leg of three survives — the recorded gitlink — and it is the one
leg a local checkout can diverge from freely.

openxFactory's own pin file, which D1 studies and quotes, says this in as many
words: "The gitlink commit fixes these bytes as strongly: **the verifier compares
BOTH the recorded gitlink and the checked-out revision against `commit:` above**,
so a swap of any of these files is a swap of the commit. Presence is checked
here; identity comes from the commit." — and `scripts/validate-openxwallet.py` is
in that very `pinned_by_commit_only` list. D1 imports the conclusion ("the
gitlink commit IS the content address") while declining to build the verifier the
conclusion rests on.

This also falsifies the proposal's headline benefit at `proposal.md:93-101`:
"The descendant makes 'which reader ran' answerable by a pin instead of by a
directory walk." It makes it answerable by a **declaration**. `neutral-product-pin`
words the standard: "so that WHICH READER RAN is an auditable digest rather than
an assumption", and "The pin's digests SHALL be verified BEFORE the pinned reader
is invoked, **by running code rather than by a stated obligation**".

**EVIDENCE.**
- `openxFactory origin/main:contracts/openxwallet-pin.yaml` —
  `verify_pin: scripts/verify-openxwallet-pin.py`, `resync_runbook:
  openXwallet/docs/pin-resync-runbook.md`, and the `pinned_by_commit_only`
  comment block quoted above
- `openxFactory origin/main:openspec/changes/split-openxwallet-repo/design.md:406-410`
- `openxFactory origin/main:openspec/changes/split-openxwallet-repo/specs/neutral-product-pin/spec.md`,
  requirement "A required check runs the pinned tool, at the pinned digest" and
  its scenario "The pinned reader runs before the pin is verified → the check is
  a green result over unverified bytes and is refused"
- `design.md:100-106` (D1's rejection of the digest block)

**REQUIRED CHANGE.** LedgerxWallet ships a `verify_pin:` — running code that
compares BOTH the recorded gitlink AND `git -C openXwallet rev-parse HEAD`
against `contracts/openxwallet-pin.yaml`'s `revision`, refusing before the
pinned validator is invoked — or the packet adopts the eight digests D1
rejected. Either is acceptable; neither is optional. Restate
`proposal.md:93-101`'s benefit as "declared, and verified by <named code>",
never as "answerable by a pin" alone.

---

### V4 — The ratified enforcer is the DESCENDANT'S OWN validator; the packet puts the check only in LedgerxFactory

**IMPACT: HIGH**

**ATTACK.** Rule 2's ratified scenario names its enforcer: "**WHEN** a
descendant's `contracts/<product>-pin.yaml` and its nested gitlink name
different commits of the product **THEN** the **descendant's own validator**
REFUSES the tree rather than preferring either." The packet places the pin
comparison exclusively in `LedgerxFactory/tests/validate_wallet_estate.py`
(`tasks.md` 5.4, D7). Task 4.3's three mechanical changes to the moved validator
add no pin check at all.

Consequence, concretely: clone LedgerxWallet standalone, edit
`contracts/openxwallet-pin.yaml`'s `revision` without moving the gitlink, run
`python3 tests/validate_wallet_estate.py` in the descendant. Nothing refuses.
The descendant — the artifact the ratified rule binds — has no pin enforcement of
its own; the enforcement is in the consumer, which is the one place the ratified
scenario does not put it. The packet's own spec delta at `:28-31` ("**THEN** the
tree is REFUSED rather than either being preferred") therefore names no enforcer
inside the repository whose tree it is talking about.

**EVIDENCE.**
- `openxFactory origin/main:openspec/changes/split-openxwallet-repo/specs/domain-descendant-boundary/spec.md`,
  requirement "A descendant pins the product by commit, twice", scenario "The pin
  manifest and the gitlink disagree"
- `tasks.md:168-176` (5.4, the delegator holds the three-way read)
- `tasks.md:137-146` (4.3, the moved validator's three changes — no pin check)
- `specs/ledgerxwallet-overlay-boundary/spec.md:28-34`

**REQUIRED CHANGE.** Add the pin-agreement refusal to the DESCENDANT'S validator
as a fourth mechanical change, and let the delegator read `stack.yaml`'s third
declaration only. Then the ratified enforcer exists where the rule puts it, and
the delegator's remaining job is one comparison rather than three.

---

### V5 — The spec delta swaps the ratified fork-detector from "digests" to "recorded commit", while claiming to issue no delta

**IMPACT: MEDIUM**

**ATTACK.** Ratified rule 3's scenario: "**THEN** the descendant is a fork, the
copy is refused, and **the pin's digests are what detect it**." The packet's
delta rewrites it: `specs/ledgerxwallet-overlay-boundary/spec.md:100-102` —
"**THEN** the descendant is a fork, the copy is refused, and **the pin's recorded
commit is what detects it**." Meanwhile `proposal.md:333-340` declares "Modified
Capabilities: None … It does not amend them".

Substituting the enforcement basis of a ratified scenario is an amendment
whether or not a delta file says so — and the substitute does not work. A
gitlink commit detects nothing about a file placed OUTSIDE `openXwallet/`: put an
edited copy of `openxwallet-record.schema.yaml` at
`LedgerxWallet/schemas/openxwallet-record.schema.yaml` and no declared check in
this packet compares LedgerxWallet's tree against openXwallet's content. The
scenario asserts a detector the packet declined to build (V3).

**EVIDENCE.** the two spec texts above; `proposal.md:333-340`; `design.md:100-106`.

**REQUIRED CHANGE.** Either quote the ratified scenario unchanged and record in
`design.md` that the digest-based detector is UNBUILT and its absence is a named
successor, or build it. Do not reword a ratified enforcement basis inside a
change that declares it issues no delta.

---

### V6 — "An empty wallet descendant … is REPORTED" names no reporter, in the packet's own normative text

**IMPACT: LOW**

**ATTACK.** `proposal.md:296-300` congratulates the packet for removing exactly
this shape: "an earlier draft of this section said it would be 'REPORTED' and
named no reporter, which is the LS-A3 shape." Its own spec delta then commits it:
`specs/ledgerxwallet-overlay-boundary/spec.md:169-171` — "**WHEN** a
`<Domainx>Wallet` repository exists carrying no wallet profile artifact **THEN**
it is an empty boundary, and it is **REPORTED** rather than cited as precedent
for creating more." No reporter exists. There is no CI in either repository, no
enumeration that sees a nested descendant (D2), and no task that creates one.
The wording is inherited from the ratified parent — which softens it — but the
parent used lower-case prose in a rule about a class, while this delta
capitalizes it as this capability's own scenario.

**EVIDENCE.** the two paths above; `tasks.md:238-240` (7.4, "No LedgerxFactory
GitHub Actions workflow"); `design.md:130-138` (D2, outside every enumeration).

**REQUIRED CHANGE.** Name the reporter or drop the verb: "it is an empty
boundary, and it SHALL NOT be cited as precedent" states the same rule with no
unowned enforcement.

---

### V7 — Tasks 6.3–6.6 prove refusals; the one assertion that proves the estate was READ is deleted

**IMPACT: HIGH**

**ATTACK.** The packet's four RED proofs (6.3 mutate a pin, 6.4 uninitialized
submodule, 6.5 estate root with no `tenants/*/wallets/`, 6.6 no gitlink) are all
NEGATIVE: they prove the validator refuses when something is missing. The only
POSITIVE assertion — that the governed surface was actually opened — is the
`repo scan: >= 5` count, which V1 shows cannot survive and which no task
replaces. Task 6.2's wording is "the wallet estate reached THROUGH the
delegator" — reached, not read.

`neutral-product-pin` legislates precisely this distinction: "The LITERAL
invocation string SHALL be pinned in a test in the consuming repository, and
that test's assertion SHALL be POSITIVE — that the intended governed surface WAS
read — never merely that an argument was present", with the scenario "**WHEN** the
consuming repository carries no test asserting the required check's literal
invocation and that the governed surface was read **THEN** nothing prevents a
silent repoint to a target that reads nothing, and the enforcement claim is
UNMET". And: "**WHEN** the scan target passed to the pinned validator is the
product's own pinned directory rather than the consuming repository's root
**THEN** the consuming repository's governed surface is never opened, and the
check refuses" — which is exactly the failure mode a validator whose `REPO` is
now the descendant walks into.

**EVIDENCE.** `tasks.md:206-222` (6.1-6.6); `tests/validate_wallet_estate.py:725-729`;
`openxFactory origin/main:openspec/changes/split-openxwallet-repo/specs/neutral-product-pin/spec.md`,
requirement "A pinned validator invoked with no scan target refuses".

**REQUIRED CHANGE.** Add a POSITIVE proof to §6: the literal invocation string
pinned in a test, plus an assertion on the re-derived record count AND on the
specific record ids adjudicated, in both trees. A refusal proof and a read proof
are different proofs and the packet currently owns only the first kind.

---

### V8 — The fail-closed remediation drops the pin-resync runbook the ratified rule requires, and the pin file carries neither `verify_pin:` nor `resync_runbook:`

**IMPACT: MEDIUM**

**ATTACK.** Ratified: "Every such refusal SHALL carry a REMEDIATION STRING
naming the initializing command (`git submodule update --init <product-dir>`)
**and the path of the pin-resync runbook**, so the exit is in the message rather
than in tribal memory." The packet's spec delta at `:122-125` requires only "a
REMEDIATION STRING naming the initializing command", and its restatement of the
ratified defect scenario at `:139-141` narrows to "emits a refusal that names no
command" — the runbook half is gone from both. No task creates a pin-resync
runbook for LedgerxWallet, and `tasks.md` 3.4's field list for the pin file omits
both `verify_pin:` and `resync_runbook:` — the two fields openxFactory's own pin
carries, one of which that file annotates "NAMED here so the pin is running code
rather than an obligation stated in prose (clarification N3)".

**EVIDENCE.** ratified `neutral-product-pin`, requirement "An unanswerable pin
question refuses, and the refusal names its remedy";
`specs/ledgerxwallet-overlay-boundary/spec.md:122-125,139-141`;
`tasks.md:107-115` (3.4); `openxFactory origin/main:contracts/openxwallet-pin.yaml`
(`verify_pin:`, `resync_runbook:`).

**REQUIRED CHANGE.** Restore "and the path of the pin-resync runbook" to both
spec passages; add `verify_pin:` and `resync_runbook:` to 3.4's field list; add a
task authoring `LedgerxWallet/docs/pin-resync-runbook.md`.

---

## Pin-skew findings — six declarations, and the ones nobody counted

### V9 — The three-way invariant is self-consistent by construction and blind to the only drift that matters: WHICH LedgerxWallet commit

**IMPACT: HIGH**

**ATTACK.** D7 names three declarations of the openXwallet commit and requires
agreement. All three are read out of **whatever LedgerxWallet commit the
LedgerxFactory gitlink happens to name**. Nothing declares that commit anywhere —
`stack.yaml` gains no `ledgerxwallet:` block, and the `openxwallet:` block
declares the *product*, not the *descendant*.

Skew scenario, fully concrete. LedgerxWallet bumps its pin correctly: gitlink and
manifest move together to openXwallet commit `Y`, one commit, ratified rule
honoured. LedgerxFactory does not bump its `LedgerxWallet` gitlink and does not
touch `stack.yaml`. The delegator now reads the OLD LedgerxWallet checkout:
gitlink `63f5a1ad`, manifest `63f5a1ad`, `stack.yaml` `63f5a1ad` — **three-way
agreement, GREEN** — and validates the estate against a superseded contract while
the descendant's `main` pins `Y`. D7's stated property ("after this change the
commit governing the Ledgerx estate is the one LedgerxWallet pins") is FALSE in
this state, and the invariant cannot detect it because all three of its inputs
travel together inside the stale submodule.

Compare `xfactory:` at `stack.yaml:14-17`, which DOES declare
`contract_ref: af7ac0fa…` + `contract_source:` so openxFactory staleness is
detectable from LedgerxFactory's own tree. The descendant is given no such
declaration, which is a strict regression in the one direction P6 introduces.

**EVIDENCE.** `design.md:261-274` (D7's three declarations);
`LedgerxFactory origin/main:stack.yaml:14-17` (the `xfactory:` pattern) and
`:51-59` (the `openxwallet:` block, `contract_source:
openxFactory-nested-submodule-pin` at `:59`); `tasks.md:168-176` (5.4).

**REQUIRED CHANGE.** Add a FOURTH declaration and put it in the invariant:
`stack.yaml` gains `ledgerxwallet:` with `contract_ref` = the LedgerxWallet
commit, mirroring `xfactory:`, and the delegator refuses when the initialized
`LedgerxWallet` gitlink disagrees with it. Without a declaration of the
descendant's own commit, the three-way check is a comparison of three copies of
one field.

---

### V10 — After the move the descendant reads LedgerxFactory's openxFactory pin and echoes relocation notices about a DIFFERENT openXwallet commit than the one validating the estate

**IMPACT: HIGH**

**ATTACK.** The moved validator invokes openxFactory's pin checker
(`OPENXFACTORY_DIR`/`PIN_CHECKER_PATH`, `:132-133`), extracted at
`stack.yaml["xfactory"]["contract_ref"]` from the openxFactory checkout that
`find_aggregation()` resolves — the **aggregation's** openxFactory, reached by
directory adjacency from inside a descendant (V2). That pinned openxFactory
bundle carries its OWN `contracts/openxwallet-pin.yaml` with `commit:` and eight
`sha256` rows, and the notice the bar echoes concerns THOSE rows.

So after P6 a single bar run reads **two independent openXwallet truths** — the
one openxFactory pins (declaration 4/5) and the one LedgerxWallet pins
(declarations 1/2/3) — prints the first as an observation, validates the estate
with the second, and compares them never. D7 authorizes the non-comparison
("Divergence is therefore not an error and is not checked"), which is a defensible
decision; what is not stated is that the packet keeps a **reporter** whose subject
is the un-compared pin. Skew: openxFactory bumps to `wallet-v2.0` with relocating
rows; the bar prints a deprecation notice naming contract rows the Ledgerx estate
does not consume; the operator reads it as advice about their own pin. That is
worse than silence, because it is a green run carrying a notice about the wrong
tree — the "wrong-target default" hazard the same file's own probe set names
(`:489-491`, probe `wrong-target`).

**EVIDENCE.** `tests/validate_wallet_estate.py:121-133` (the emitter rationale
and constants), `:598-660` (`check_pin_reconciliation` docstring, "REPORTED, NOT
ENFORCED"), `:675-689`, `:489-491`;
`openxFactory origin/main:contracts/openxwallet-pin.yaml` (`commit:
63f5a1ad…`, eight `sha256` rows, `contract_bundle_tag: wallet-v1.1`);
`design.md:283-295` (D7's fourth/fifth declarations).

**REQUIRED CHANGE.** Decide which repository owns the openxFactory relocation
observation. It belongs in LedgerxFactory (it reads LedgerxFactory's
`stack.yaml` and the aggregation) and must NOT travel into the descendant. State
in D7 that the notice's subject is openxFactory's pin and not the descendant's,
and make the printed line say so.

---

### V11 — A THIRD reachable openXwallet checkout falls THROUGH `neutral-product-pin`, and the ratified "resolves the NESTED checkout" scenario becomes false for this consumer

**IMPACT: MEDIUM**

**ATTACK.** The ratified rule's equality obligation names exactly two gitlinks:
"the aggregation's ROOT gitlink for a product `openxFactory` pins SHALL EQUAL
`openxFactory`'s NESTED gitlink commit, checked in the aggregation." P6 adds a
third reachable checkout at `xFactories/LedgerxFactory/LedgerxWallet/openXwallet`.
It is inside no equality obligation, and — answering the quarry directly — it
falls THROUGH: nothing requires it to equal either governed gitlink, and the
aggregation's check (`verify-openxwallet-pin.py --aggregation-root`, parent D11)
does not know it exists.

The sharper consequence is that the same capability's *other* requirement now
states something false about this tree: "**WHEN** a walk-up resolver in a
consumer repository can reach both the aggregation's root checkout of the product
and `openxFactory`'s nested checkout **THEN** it resolves the NESTED checkout".
After P6 a walk-up resolver in the Ledgerx tree can reach three, and must resolve
NONE of them — it must resolve the descendant's. D7 dismisses the capability as
"a rule about openxFactory's consumption, not about a domain descendant's", which
is fair for the equality clause but not for this scenario, whose subject is
explicitly "a consumer repository". The packet engages the first clause and never
quotes the second.

**EVIDENCE.** `openxFactory origin/main:openspec/changes/split-openxwallet-repo/specs/neutral-product-pin/spec.md`,
requirement "The consuming repository's pin is authoritative among reachable
checkouts" and its first and third scenarios; `design.md:283-295`;
`/home/brett/projects/xFactory/.gitmodules` (root `openXwallet` absent — P4 open,
so today two reachable, three after P4).

**REQUIRED CHANGE.** Quote the "reachable checkouts" requirement in D7 and state
which of its scenarios P6 satisfies, which it makes vacuous, and which needs an
amendment to `split-openxwallet-repo`. A first-of-standard change that leaves a
ratified scenario factually wrong about the tree it created owes that statement.

---

### V12 — D5's estate-root guard is a PRESENCE check, and every LedgerxFactory worktree passes it

**IMPACT: MEDIUM**

**ATTACK.** D5 defaults the estate root to `..` and guards it with "REFUSES with
a named exit when that root holds no `tenants/*/wallets/` directory". Find the
trees where `..` is wrong and the refusal does not fire:

LedgerxFactory has multiple live Speckit worktrees — `git worktree list` shows
`LedgerxFactory-worktrees/002-subject-onboarding-readiness` (`cf4ac7b`),
`…/003-neutral-books-design` (`09b2b2b`), alongside the canonical checkout at
`a645858`. Every one of them carries `tenants/ledgerxcorp/wallets/`. Initialize
`LedgerxWallet` inside any of them and `..` resolves to that worktree — the
guard is satisfied, and the descendant silently validates a **stale branch's**
estate. Nothing distinguishes "an estate root" from "the estate root": the check
tests that a directory pattern exists, not that this is the tree whose
`stack.yaml` declares the pin the delegator just verified.

That is verbatim the error the governing capability names: "PRESENCE IS NOT
IDENTITY: a file-existence check is not a verification". D5's own sharp-edge
discussion covers only the `xFactories/` placement — where the refusal DOES fire
— and misses the case where it does not.

**EVIDENCE.** `design.md:222-241` (D5); `git -C
/home/brett/projects/xFactory/xFactories/LedgerxFactory worktree list` output
above; ratified `neutral-product-pin`, requirement "A vendored foreign contract
is digest-verified before it is read" ("PRESENCE IS NOT IDENTITY…").

**REQUIRED CHANGE.** The estate-root guard must assert IDENTITY, not presence:
the resolved root's `stack.yaml` must exist, parse, and carry
`openxwallet.contract_ref` equal to the descendant's pin `revision`. Then a wrong
tree refuses instead of validating.

---

### V13 — The declaration nobody counted: `stack.yaml` is DIGEST-PINNED, task 5.5 edits it, and task 5.9 says no re-pin is owed

**IMPACT: HIGH**

**ATTACK.** `tasks.md` 5.9 states: "`models/protected-surface.yaml`'s PROSE
mention at `:438` — a pointer amendment only. **Verified: that file carries NO
digest row for any of the three moved paths, so no digest re-pin is owed.**" The
inference is correct about the three moved paths and then generalized. Task 5.5
edits a FOURTH file: `stack.yaml` — which IS a pinned file with a digest row.

`models/protected-surface.yaml:384-386`:

```yaml
  - path: stack.yaml
    digest: "5f589a7d095aedba85f41ad07d16158b665090e21cbe6a8147280eba39a4b8bc"
    pinned_by: >-
      Re-pinned 2026-08-27 (second bump that day) IN THE SAME COMMIT as
      the change that modified the file.
```

`tests/validate_onboarding_contracts.py:489-502` recomputes every pinned file's
sha256 and errors `"%s diverges from its pinned digest"`. So the §5 one-commit
lands with `stack.yaml` edited and its digest stale: `validate_onboarding_contracts.py`
goes RED on `main`, and task 6.2's "bar green" is unreachable. The repository has
already paid for this exact omission once — that same entry records "The unpinned
window showed as `[baseline] stack.yaml diverges from its pinned digest` in
validate_onboarding_contracts.py, **red on main for seventeen days**" — and
`docs/protected-surface.md:66-69` states the rule: "## Modifying a file that is
already pinned / Unchanged by any of the above: edit it, **recompute its digest**,
and update the entry with the reason recorded beside it."

**EVIDENCE.** `models/protected-surface.yaml:383-387` and `:445-449` (the
seventeen-day record); `tests/validate_onboarding_contracts.py:486-502`;
`docs/protected-surface.md:66-69`; `tasks.md:177-181` (5.5) and `:198-202` (5.9).

**REQUIRED CHANGE.** Task 5.9 gains: recompute `stack.yaml`'s sha256 and re-pin
it in `models/protected-surface.yaml` **in the same commit**, with `pinned_by`
citing this change. Replace 5.9's over-general sentence with "no digest re-pin is
owed **for the three moved paths**; `stack.yaml` IS pinned and its re-pin is part
of this commit."

---

## Also attacked

### V14 — D4 and D7 are mutually inconsistent: the delegator that "computes no answer" computes three-way agreement

**IMPACT: MEDIUM**

**ATTACK.** D4's fork-freedom argument is: "The delegator re-authors nothing: it
holds no rule that could disagree with the implementation, and the failure mode a
fork creates — two answers to the same question — is unavailable to **a file that
computes no answer**." D7 then gives that same file a computation: "The delegating
bar entry (§ D4) **reads all three and REFUSES on any disagreement**", and
`tasks.md` 5.4 makes it explicit — "read and compare the THREE pin declarations
(D7) and refuse on disagreement". A file that reads three declarations, compares
them, and decides whether to refuse **does** compute an answer, and it is the
answer to the question "which openXwallet commit governs this estate". A second
implementation of that comparison in the descendant (V4 requires one) would then
be exactly the "two answers to the same question" D4 says is unavailable.

D4's conclusion still holds on a better argument — the delegator holds no RULE OF
THE PRODUCT — but the argument the packet actually makes is falsified by its own
next decision, and `tasks.md` 4.6 promises to "Prove the fork-freedom property D4
names: every rule, threshold, expected set and probe corpus appears in EXACTLY
ONE file across both repositories." A pin comparison in two files fails that grep.

**EVIDENCE.** `design.md:196-202` (D4), `:275-281` (D7); `tasks.md:168-176` (5.4),
`:154-156` (4.6).

**REQUIRED CHANGE.** Re-state D4's argument as "the delegator holds no rule OF
THE PINNED PRODUCT and no expected set" and delete "computes no answer". Then
decide where the single pin comparison lives (V4 says the descendant) and have
the other side call it rather than reimplement it.

---

### V15 — D9's repoint is NOT links-only: the quickstart's prerequisite, its bar command, and its evidence requirement all change

**IMPACT: HIGH**

**ATTACK.** D9 and `tasks.md` 5.6 promise "LINKS ONLY: no step, actor, abort
condition or evidence requirement is touched", and name `quickstart.md:15`. The
file's actual wallet content is not at `:15` and is not links:

- `:4-5` — a PREREQUISITE: "the pinned openxFactory checkout at the workspace
  root, **with its nested `openXwallet` gitlink initialized**". After P6 that
  prerequisite is false; the required initialization is
  `LedgerxWallet`/`LedgerxWallet/openXwallet`. A precondition is not a link.
- `:19` — inside "## The bar (every commit on this branch)":
  `python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`.
  That is a documented BAR COMMAND, and after P6 it is the resolution the
  packet's own spec delta refuses (`spec.md:59-61`). Repointing it is a step
  change.
- `:23` — an EVIDENCE REQUIREMENT: "The wallet validator must report the new
  records under `tenants/ledgerxcorp/wallets/` as validated artifacts (not
  skipped) — see [data-model.md](data-model.md) for the expected instance set."
  Moving the DHC out of that directory changes the expected instance set from
  five to four (V1). That is exactly an evidence requirement touched.

And the paired links at `runsheet.md:23,25` split: the template moves, the
holder-registry schema stays (D3a), so one of two adjacent relative links now
crosses a repository boundary while the other does not — in a procedure whose
operator is Brett, with an ADMIN and an OPSX lane and real key minting.

**EVIDENCE.** `specs/016-posting-segregation-of-duties/quickstart.md:4-5,19,23`;
`specs/016-posting-segregation-of-duties/runsheet.md:1-3` (`Status: prepared`),
`:23`, `:25`; `design.md:324-344` (D9); `tasks.md:182-190` (5.6).

**REQUIRED CHANGE.** Correct the line anchors, and drop the "LINKS ONLY" claim:
enumerate the three quickstart edits (prerequisite, bar command, expected
instance set) as what they are. Then task 5.7's "tell the window's operator" must
say WHICH of those three changed, because the operator's abort conditions read
off the expected instance set.

---

### V16 — References beyond feature 016 are un-repointed, including two live rollback procedures and a documented module import

**IMPACT: MEDIUM**

**ATTACK.** D9 scopes the repoint to feature 016. The tree carries more:

- `specs/017-openxwallet-finder/quickstart.md:36,49` — `import
  validate_wallet_estate as v` then `v.run_validator(v.REPO, strict=True)` and
  `v.check_finder_candidates()`; and `:97-98` — `cp
  tests/validate_wallet_estate.py "$T/tests/" && python3
  "$T/tests/validate_wallet_estate.py"`. After P6 that path is a delegator with
  no `REPO`, no `run_validator`, no `check_finder_candidates`. The documented
  reproduction procedure for a merged feature breaks silently.
- `specs/019-openxwallet-consumer-repoints/rollback.md:37` — "**`tests/validate_wallet_estate.py`**
  — restore the THIRD candidate"; `specs/018-openxwallet-pin-bump/rollback.md:28`
  — "**`tests/validate_wallet_estate.py`** — delete …". Both are rollback
  procedures for MERGED features, and both operate on a file P6 replaces. After
  P6 the wave cannot unwind P5b or P5a.2 by its own recorded procedure — which
  contradicts D10's "rollback is a revert rather than a recovery".
- `specs/016-posting-segregation-of-duties/tasks.md:215` names
  `templates/wallet-exercise.template.yaml`; `:91` and `:127` name
  `tests/validate_wallet_estate.py`;
  `specs/016-.../negative-confirmations.md:43` — "Registered in
  `tests/validate_wallet_estate.py`, which materializes …" — a feature-016
  deliverable whose statement becomes false while its owning change is still
  ACTIVE.

**EVIDENCE.** all paths and lines above, read on `LedgerxFactory origin/main`.

**REQUIRED CHANGE.** Either widen §5.6 to a declared inventory of every
reference to the three moved paths (the grep is four lines and I ran it), or
state explicitly in D9 that records of PERFORMED acts keep their historical
paths and add a dated note to 017/018/019 saying so — and in either case say
what happens to P5b's rollback.

---

### V17 — D3's test classifies dozens of artifacts wrongly, not one; D3a is a symptom, not the exception

**IMPACT: HIGH**

**ATTACK.** D3: "An artifact belongs in `LedgerxWallet` if and only if it would
be IDENTICAL for a second Ledgerx tenant." Applied to the LedgerxFactory tree
that test pulls in most of the repository. Two concrete second artifacts, and
they are not edge cases:

- `policies/posting-autonomy.template.yaml` — `kind: ledgerx_posting_autonomy`,
  header "Instantiation stub — tenant declares default + range once", body
  `domain_invariants` / `tenant_default` / `tenant_permitted_range`. Names no
  tenant; identical for a second Ledgerx tenant; subject matter is posting
  authority, which is what the wallet grants gate. D3's test says LedgerxWallet.
  It is also a digest-pinned member of a PROTECTED DIRECTORY
  (`models/protected-surface.yaml:349-350`; `protected_directories: - path:
  policies`), and its tenant instance
  `policies/ledgerxcorp-posting-autonomy.yaml` would stay — splitting a
  template/instance pair across repositories, the very seam D3 exists to avoid.
- `templates/environment-wide-act.yaml` — "Instantiation stub … FICTIONAL
  values". Identical for a second tenant. So are 34 of the other 35 files in
  `templates/`, plus every `policies/*.template.yaml`, plus `conformance/`, plus
  `hermes/domain/`.

D3a's justification is the right discriminator and it exposes what the test is
missing: the holder registry stays because "its counterparty is the ENFORCING
PLATFORM, not the pinned product." The test needs that conjunct — *and it is an
interpretation of the pinned product* — or it is not a test, it is a list with one
exception written down and thirty more unwritten. This matters more than any
single misfiling because `design.md:386-390` names D3 as the packet's
generalizable contribution: "Whatever this packet gets wrong becomes the shape
three more domains copy — which is the argument for the decidable test in D3
rather than a list of three files."

**EVIDENCE.** `LedgerxFactory origin/main:policies/posting-autonomy.template.yaml:1-5`;
`templates/environment-wide-act.yaml:1-4`; `git ls-tree` of `templates/` (36
files); `models/protected-surface.yaml:29-33,349-350`; `design.md:147-171` (D3,
D3a), `:386-390`.

**REQUIRED CHANGE.** Restate D3 as a CONJUNCTION: an artifact belongs in the
descendant iff (a) it would be identical for a second tenant of this domain AND
(b) it is an interpretation of the PINNED PRODUCT's vocabulary. Then D3a stops
being an exception and becomes an application, and the test survives contact with
`MedxWallet`.

---

### V18 — A second bar validator declares the old consumption path, and task 5.8 amends only the kind row beside it

**IMPACT: LOW**

**ATTACK.** `tests/validate_document_estate_surface.py:1094-1099`: "This
repository declares the bundle it consumes in its own stack.yaml `openxwallet:`
block, and **the validator runs from openxFactory's nested gitlink
(openxFactory/openXwallet/scripts/validate-openxwallet.py) — see
find_openxfactory() in tests/validate_wallet_estate.py for the ordered
candidates.** Corrected at P5b: ratified split-openxwallet-repo tasks.md 10.6,
feature 019-openxwallet-consumer-repoints."

After P6 that block names a consumption path the tree no longer takes and a
function that no longer exists — and it is a P5b-RATIFIED correction, so leaving
it stale re-opens the defect P5b closed. `tasks.md` 5.8 amends only the
`ledgerx_wallet_exercise_template` registration eleven lines below it. This is
the same defect the packet refuses elsewhere: `proposal.md:284-288` — "a
`contract_source` naming openxFactory's gitlink would describe a consumption path
the tree no longer takes."

Separately, task 5.8's premise is overstated. The archived ratified change
`2026-08-27-modify-ledgerx-document-estate-warrant-scope/design.md:148-153`
already ruled on these entries: "The wallet kinds registered by feature 016
(`ledgerx_wallet_holder_registry_contract`, `ledgerx_wallet_exercise_template`)
stay … **They are now vestigial under this warrant**, which is a tidiness question
for the wallet lane and not this change's to settle." P6 is entitled to settle it
(it IS the wallet lane), but "leaving it would be a stale registration in a
surface gate" overstates the consequence of an entry a ratified change already
called vestigial.

**EVIDENCE.** `tests/validate_document_estate_surface.py:1085-1121`;
`openspec/changes/archive/2026-08-27-modify-ledgerx-document-estate-warrant-scope/design.md:148-153`;
`tasks.md:193-197` (5.8); `proposal.md:284-288`.

**REQUIRED CHANGE.** Extend 5.8 to the comment block at `:1085-1099`, and cite
the archived ruling when amending the registration so the disposition is
traceable rather than re-decided.

---

### V19 — Deleting `VALIDATOR_CANDIDATES` destroys the PARENT's own realization evidence, and 4.3's "byte-unchanged probe corpora" is false

**IMPACT: HIGH**

**ATTACK.** Task 4.3(a) deletes `VALIDATOR_CANDIDATES` and the walk. That
deletion also removes, unnamed anywhere in the packet:

- `check_finder_candidates()` and its eight `FINDER_PROBES` (`:304-331`) —
  including the assertion `if declared != [_NESTED, _AGGREGATION]: err(…
  "drifted from ratified split-openxwallet-repo D9 as narrowed by tasks.md
  10.1")`, and the `legacy-only` probe whose INVERSION the file calls "the whole
  of what 10.1 changes observably";
- `check_finder_loud_failure()` (`:377-401`), whose docstring names its
  authority: "Ratified split-openxwallet-repo tasks.md 2.3 — 'a loud failure,
  never a skip'";
- the constants `_NESTED`, `_AGGREGATION`, `_LEGACY`, retained at P5b precisely
  "because the valuable fact about this path is now that it must resolve NOTHING".

These are the running realization evidence of the parent's ratified tasks 2.1-2.3
and 10.1, and the parent **has not archived** — it archives on "merged plus green
realization evidence" (`tasks.md` 13.1: "Fill EVERY cell of the
realization-evidence table — it is a gate, not a report"). P6 deletes its
parent's evidence before its parent's gate closes.

And `tasks.md` 4.3's claim is factually false as written: "`EXPECTED_CONSTRAINT`,
`ENVIRONMENT_EVIDENCING`, `PLATFORM_VERIFIABLE`, `PIN_VERDICTS` and **every
negative-probe corpus** are BYTE-UNCHANGED." `FINDER_PROBES` is a negative-probe
corpus (two of its eight probes assert `None`) and it cannot survive 4.3(a).
Task 6.6 replaces one of the eight probes; the other seven and the ratified
order assertion have no successor.

**EVIDENCE.** `tests/validate_wallet_estate.py:53-78, 275-331, 352-374, 377-401`;
`tasks.md:137-146` (4.3), `:219-222` (6.6);
`openxFactory origin/main:openspec/changes/split-openxwallet-repo/tasks.md:1443-1445`
(13.1).

**REQUIRED CHANGE.** State in `design.md` D5 exactly which checks die with the
tuple, and either (a) sequence P6's realization AFTER the parent archives, or (b)
migrate the probes: the parent's ratified precedence properties become
LedgerxWallet's "the single candidate resolves, and NOTHING above it does" probe
set, with the P5b `legacy-only`/`nothing-found` inversions preserved. Then fix
4.3's byte-unchanged sentence.

---

### V20 — `profile/custody-posture.yaml` puts the ceiling in two places and defeats task 4.6's own proof

**IMPACT: HIGH**

**ATTACK.** D8 declares the posture as YAML: "`custody.model: holder_readable`,
environment-evidencing, authority ceiling `act`". The moved validator already
holds both facts as PYTHON LITERALS, and task 4.3 declares them BYTE-UNCHANGED:

- `:142` — `ENVIRONMENT_EVIDENCING = {"holder_readable", "isolated_invocable"}`
- `:770-773` — `if tier != "act": err(f"{gid}: authority_tier {tier!r} exceeds
  the ratified environment-evidencing ceiling 'act'")`

So after 4.4 the custody model set and the authority ceiling exist twice — once
declared in `profile/custody-posture.yaml`, once enforced from literals — and
task 4.5 ("The validator checks the tenant records against 4.4's posture") does
not say the literals are replaced by reads of the posture. Task 4.6 then promises
to "Prove the fork-freedom property D4 names: every rule, threshold, expected set
and probe corpus appears in EXACTLY ONE file across both repositories. A
grep-based check". That grep FAILS on the packet's own §4: `holder_readable` and
`act` appear in both files. D8's defence — "the custody FACTS stay in the tenant
records; the posture declares what those facts are allowed to be … not a second
truth" — is correct about facts-vs-posture and silent about posture-vs-literal,
which is where the second truth actually lands.

**EVIDENCE.** `tests/validate_wallet_estate.py:141-150, 750-773`;
`design.md:297-320` (D8); `tasks.md:147-156` (4.4, 4.5, 4.6).

**REQUIRED CHANGE.** Task 4.3 gains a fourth mechanical change: `ENVIRONMENT_EVIDENCING`,
`PLATFORM_VERIFIABLE` and the `"act"` ceiling are READ from
`profile/custody-posture.yaml` and cease to be literals — which is what makes 4.6
provable and what makes D8 worth doing. Otherwise cut 4.4 to the successor D8
already says costs nothing else.

---

### V21 — The new repository's CODEOWNERS omits the directory the packet moves an artifact into, and no floor names the pin file

**IMPACT: MEDIUM**

**ATTACK.** Task 3.3 scopes LedgerxWallet's CODEOWNERS to `/contracts/`,
`/profile/`, `/tests/` and `/.github/`. Task 4.1 places
`templates/wallet-exercise.template.yaml` at `templates/` — a fifth directory,
unowned. So the one moved artifact a prepared live window instantiates records
from lands outside owner review in a repository created specifically to govern
it. `README.md` — which D10 makes the SOLE carrier of the provenance that `git
log` loses — is also unowned, so prose provenance is editable without review.

Separately, `neutral-product-pin`'s last requirement: "The pin file and the
gitlink SHALL therefore be named in the consuming repository's **merge-gate floor
as never-clearable paths**", and the parent's D10 realized exactly that for
codexFactory (`never_clearable_paths` gains `contracts/openxwallet-pin.yaml` and
`openXwallet`). LedgerxWallet is created with a branch-protection ruleset and no
floor; LedgerxFactory has neither (`tasks.md` 7.4). `proposal.md:386-390` asserts
"P3b — codexFactory's merge-gate floor — is codexFactory's. P6 touches neither
surface" without testing whether the requirement reaches a descendant that pins
the same product.

**EVIDENCE.** `tasks.md:102-106` (3.3), `:129-132` (4.1), `:238-240` (7.4);
`LedgerxFactory origin/main:.github/CODEOWNERS` (ten path lines; no
`/templates/`, `/tests/`, `/models/`);
ratified `neutral-product-pin`, requirement "Repointing the reader and editing
what it reads is one human-only act";
`split-openxwallet-repo/design.md:400-404` (D10).

**REQUIRED CHANGE.** Add `/templates/` and `/README.md` to 3.3's CODEOWNERS
scope. Add a task that either names `contracts/openxwallet-pin.yaml` and
`openXwallet` as never-clearable in LedgerxWallet, or records in `design.md` why
the ratified floor requirement does not reach a descendant — with a citation, not
an assertion.

---

### V22 — The "issues no delta" posture is valid only while the parent is unarchived, and the parent's own gate does not wait for P6

**IMPACT: MEDIUM**

**ATTACK.** `proposal.md:333-340` rests on a verified present-tense fact:
`domain-descendant-boundary` and `neutral-product-pin` "are ratified by
`split-openxwallet-repo` and **not yet promoted into `openspec/specs/`**". The
parent's closing gate is `tasks.md` 13.1 — "P2 (three rows), P2b, P2.5, P3 (three
rows), P3b, P4, P4b, P5a.1, P5a.2, P5b (two rows), plus the two RULESET-STATE
rows" — and **P6 is not in it**; group 12's only task is `[GOVERNANCE]` "Open
`create-ledgerxwallet-overlay-boundary`", which this packet discharges by
existing.

So the parent can archive at any point during P6's multi-repository Speckit
realization, promoting both capabilities into `openspec/specs/`. At that moment
P6's ADDED capability sits beside promoted requirements it restates — including
the two places where it restates them DIFFERENTLY (V5's digests→commit, V8's
dropped runbook) — and the packet's "issues no delta against them" posture becomes
a live conflict rather than a citation practice. Nothing in the packet declares an
ordering constraint against the parent's archive, and `tasks.md` 2.1's "Confirm
NOTHING ELSE gates P6" does not consider it.

**EVIDENCE.** `proposal.md:333-340`; verified `openxFactory origin/main`:
`openspec/specs/` holds 52 entries and neither capability is among them;
`openxFactory origin/main:openspec/changes/split-openxwallet-repo/tasks.md:1438-1445`
(groups 12 and 13.1); `tasks.md:85-89` (2.1).

**REQUIRED CHANGE.** Add to 2.1: record whether `split-openxwallet-repo` has
archived, and state the consequence either way. If it archives before P6's spec
delta lands, the delta must be re-read against the promoted text and any
divergence (V5, V8) becomes an explicit MODIFIED delta against the promoted
capability rather than a reworded restatement.

---

## Attacks that FAILED

Nine attacks I built and could not land. The packet defends each correctly.

1. **"The packet overstates the standing of the ratified rules."** It does not.
   `openspec/specs/` on `openxFactory origin/main` holds exactly 52 entries and
   neither `domain-descendant-boundary` nor `neutral-product-pin` is among them —
   the packet's count and claim are both exact. Every citation of them is labelled
   RATIFIED-IN-CHANGE, and `proposal.md:333-340` and the Out-of-scope entry both
   state the non-promotion. I found no place where the packet cites them as
   promoted.

2. **"The nested-only governance-visibility admission (D2) is incomplete."** It is
   complete for every enumeration I could reach.
   `scripts/doc_health/corpus.py:102-114` (`discover_repos`) admits only
   `openxFactory` plus direct children of `xFactories/`;
   `scripts/doc_health/ideation_routing.py:130` is
   `CONVENTION_DOMAIN_RE = re.compile(r"^xFactories/[^/]+$")`;
   `scripts/sync-notebooklm-books.py:670` matches
   `^\s*path\s*=\s*(xFactories/\S+)\s*$`. I then attacked the reverse — a nested
   descendant's docs LEAKING into LedgerxFactory's scan — and it fails too:
   `iter_doc_paths` rglobs from `repo_path / root` for
   `GOVERNED_ROOTS = ("contracts", "docs", "examples", "ideation", "templates")`
   (`corpus.py:39`), so `LedgerxFactory/LedgerxWallet/contracts/` is never
   reached. `fam_submodule_pin_drift` (`families.py:853-875`) reads
   `gitlink_pins(agg_root)` and so is blind to a nested gitlink — which is the
   invisibility D2 already names, not a new break.

3. **"`record-immutability` is implicated by editing a prepared runsheet."** It is
   not. `families.py:201-225` scopes the four lifecycle families to
   `ctx.docs` + `ctx.lifecycle_docs`, and the lifecycle scan set is "each OpenSpec
   change packet's `proposal.md` and its `review/` records". A Speckit
   `specs/016-*/runsheet.md` in LedgerxFactory sits under neither
   `GOVERNED_ROOTS` nor the lifecycle set. The packet never claims otherwise, and
   D9 correctly argues the case on operational-safety grounds instead. (V15 stands
   on what the edit actually touches, not on doc-health.)

4. **"The `.openspec.yaml` origin is fabricated approval provenance."** It is not.
   The id `openxFactory:adhoc:2026-08-27-create-ledgerxwallet-overlay-boundary`
   matches `proposal_origin.py:67`'s
   `ADHOC_ID_RE = ^[A-Za-z0-9_.-]+:adhoc:[A-Za-z0-9][A-Za-z0-9-]*$`, and
   `reason`/`approved_by`/`approved_on` are all non-empty, satisfying
   `:239-244`'s `adhoc-provenance-incomplete` rule. Both parent quotes are
   BYTE-ACCURATE: `split-openxwallet-repo/proposal.md:1195-1197` and
   `tasks.md:1440-1444` read exactly as reproduced. And the file goes out of its
   way to bound the approval — "THIS IS AN ADMISSION INTO THE PROPOSAL QUEUE AND
   NOT A RATIFICATION OF CONTENT" — which is the honest form.

5. **"The three moved paths are digest-pinned and the packet missed it."** They are
   not. `models/protected-surface.yaml` carries no `path:` row for any of the
   three; `tests/` is not a protected directory; the single wallet mention is prose
   inside the `stack.yaml` entry's pin history at `:455`. P5b's own evidence says
   the same (`018/evidence/suite-baseline-vs-after.txt:74`). The packet's
   verification is correct — V13 lands on a FOURTH file it edits, not on these.

6. **"The annotated-tag dereference is wrong."** It is right.
   `refs/tags/wallet-v1.1` is tag object `021cdeefbae50127946f147c23edf98c653aa4a5`
   dereferencing to commit `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`
   (`gh api repos/opensoft/openXwallet/git/tags/021cdeef…`), which equals
   openxFactory's nested gitlink and its pin's `commit:`. `tasks.md` 3.4's
   `wallet-v1.1^{commit}` instruction and its stated reason are both correct.

7. **"LedgerxWallet does not need creating / already exists."** Verified absent:
   `gh repo view opensoft/LedgerxWallet` → "Could not resolve to a Repository".
   And rule 5's gate really is satisfied only for Ledgerx — I found no wallet
   profile artifact in any sibling domain.

8. **"The README repoint list is padded."** The opposite. P5b's own §10.5 evidence
   claims "`README.md` carries **no wallet path**, and no revision of it ever has"
   (`019/evidence/estate-run.md:126-128`), but `README.md:108-109` plainly carries
   both `tenants/ledgerxcorp/wallets/` and `tests/validate_wallet_estate.py`. Task
   5.9 names exactly those two references. The packet caught something its merged
   precondition's evidence got wrong.

9. **"Q2 is decided wrongly — the tenant estate should move."** I could not build
   it. The four records carry holder ids (`agent:lx-ap-intake-creator`), DIDs
   (`did:web:xforge.us:wallets:lx-*`), key ids, `expires_at`, `issued_by`, and a
   live `state:`; D3's instance side is decisive on their own contents, and the
   counter-case (two seams) is stated rather than hidden. The recommendation
   stands.
