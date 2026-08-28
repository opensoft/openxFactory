# Council — Systems Architect

**Verdict:** PROCEED WITH CONSTRAINTS

The boundary is the right shape and no placement, profile/instance or pin-grammar
decision needs to change — and the packet self-corrected mid-review to enumerate
the pin-checker leg I expected it to have missed (D5's "three jobs", tasks 4.3a),
which is the hardest dependency in the file. But the moved validator as specified
**does not run green**: three independent, arithmetically certain breaks remain
unnamed (the `>=5` repo-scan floor, the nested-repository prune, the
`EXPECTED_CONSTRAINT` reader), and the change's own thesis is left unenforced by
two mis-sitings — the pin-agreement check lives in the consumer rather than in
the descendant's own validator, and nothing compares any submodule CHECKOUT to
the gitlink that governs it.

Read for this review: all 822 lines of `tests/validate_wallet_estate.py` on
LedgerxFactory `origin/main`; `validate_document_estate_surface.py`,
`validate_protected_surface.py`, `models/protected-surface.yaml`,
`specs/001-document-estate-read/warrant.yaml`, `stack.yaml`,
`docs/protected-surface.md`, feature 016's `runsheet.md`/`quickstart.md` and
feature 019's evidence; openXwallet `scripts/validate-openxwallet.py`
(2279 lines, `sweep_candidates`/`repo_scan`); the two ratified specs; and
openxFactory's `doc-health-reusable.yml`.

---

## V1 — The `>=5` repo-scan floor breaks arithmetically the moment the DHC leaves

**IMPACT: HIGH**

**EVIDENCE.** `tests/validate_wallet_estate.py:725-729`:

```python
m = re.search(r"repo scan: (\d+) openxWallet artifact", proc.stdout)
if not m:
    err("upstream validator output carried no repo-scan count")
elif int(m.group(1)) < 5:
    err(f"expected >=5 wallet-family records validated, saw {m.group(1)}")
```

The current count is exactly 5, measured, not assumed —
`specs/019-openxwallet-consumer-repoints/evidence/estate-run.md:104`:
`note  repo scan: 5 openxWallet artifact(s) validated, 602 document(s) skipped
as another kind`. Those five are the only openXwallet-family YAMLs in the tree:
`tenants/ledgerxcorp/wallets/` holds `wal-lx-creator-01.yaml`,
`wal-lx-poster-01.yaml`, `grant-lx-create-01.yaml`, `grant-lx-post-01.yaml` and
`dhc-lx-create-post-01.yaml` (`git ls-tree -r origin/main`), and the exercise
template is skipped because `ledgerx_wallet_exercise_template` is not in
`KIND_TO_SCHEMA` (openXwallet `validate-openxwallet.py:2102-2104`,
`if not isinstance(doc, dict) or doc.get("kind") not in KIND_TO_SCHEMA: skipped += 1`).

`tasks.md:133-136` moves the DHC out of the estate. The estate-root scan then
returns 4, `4 < 5`, and the bar REDS on its first post-move run. The packet
mentions neither the count nor the threshold: `grep -inE 'repo scan|>=5|threshold'`
over the whole packet returns only D4's "NO threshold" prose about the delegator.

**REQUIRED CHANGE.** Add a task that re-derives the floor as part of the move and
records the arithmetic (5 → 4 in the estate; the fifth artifact now lives in the
descendant). Do NOT lower the constant silently — 4.3 currently promises "NO rule
change", and a threshold is a rule. Either the floor becomes a value derived from
the estate manifest of §5.3 (preferred: it is then the same declared/committed
comparison D6 already builds) or the packet states the new literal and why.

---

## V2 — The nested-repository prune silently removes the relocated profile from all neutral validation

**IMPACT: HIGH**

**EVIDENCE.** openXwallet `scripts/validate-openxwallet.py:2064-2129`,
`sweep_candidates`: *"The sweep's YAML list, with NESTED REPOSITORIES pruned out
of the walk… So the rule is: any directory below the scan root carrying a `.git`
entry, **file or directory**, is a nested repository and is not descended into."*
The loop (`:2116-2125`):

```python
for name in dirnames:
    child = here / name
    if (child / NESTED_REPO_MARKER).exists():
        pruned.append(child)
```

`tasks.md:174-178` nests `LedgerxWallet` as a submodule at the LedgerxFactory
root, so an initialized `LedgerxWallet/` carries a `.git` file and is PRUNED from
the estate-root sweep. The moved validator runs exactly one scan —
`:721 proc = run_validator(REPO, strict=True)` — re-based on the estate root by
4.3(b). Consequence: after the move, `profile/distinct-holder-constraints/dhc-lx-create-post-01.yaml`
and `templates/wallet-exercise.template.yaml` are adjudicated by **nothing**.
Feature 019's evidence confirms the mechanism was live and benign only because
the tree then had no nested repository — `estate-run.md:117-119`: *"the Ledgerx
wallet records at `tenants/ledgerxcorp/wallets/` are not inside a submodule, so
the nested-repository prune does not reach them"* and *"The prune's own `nested
repositories pruned` NOTE does not appear, and should not: the scanned tree
contains no nested repository."* After P6 it does contain one.

This directly falsifies the packet's own spec scenario (`spec.md:108-110`): "the
descendant adds a validator that checks its own profile artifacts … against the
pinned product's schemas" — and it is the exact case `spec.md:152-154` names as a
defect ("A relocated validator silently drops an enforcement leg").

**REQUIRED CHANGE.** The moved validator must run the neutral validator TWICE —
once against the declared estate root, once against the LedgerxWallet checkout
root — and the second run is what makes the profile a validated artifact rather
than a filed one. Add the task, and add the corresponding evidence item. Note in
passing that the prune NOTE will now appear in the estate-root run
(`f.note("nested repositories pruned (not adjudicated): …")`, `:2074-2076`) and
is a `note` not a `warn`, so `--strict` stays green — that part is safe.

---

## V3 — The `EXPECTED_CONSTRAINT` check reads the estate directory, so the DHC's relocation reds it

**IMPACT: HIGH**

**EVIDENCE.** `tests/validate_wallet_estate.py:731-746` populates `constraints`
by listing `WALLET_DIR` only:

```python
for fn in sorted(os.listdir(WALLET_DIR)):
    ...
    elif kind == "xfactory_wallet_distinct_holder_constraint":
        constraints[doc.get("constraint_id")] = doc
```

and `:774-776`:

```python
dhc = constraints.get(EXPECTED_CONSTRAINT)
if dhc is None:
    err(f"missing distinct-holder constraint {EXPECTED_CONSTRAINT}")
```

`tasks.md:144-145` states `EXPECTED_CONSTRAINT` is "BYTE-UNCHANGED" and lists
only three mechanical changes plus 4.3a's re-basing. Both are true and both are
insufficient: the CONSTANT can be byte-unchanged while its READER is pointed at
the wrong tree. After the move the DHC is at
`LedgerxWallet/profile/distinct-holder-constraints/`, `constraints` is empty, and
`err("missing distinct-holder constraint dhc-lx-create-post-01")` fires. D6
(`design.md:290-291`) says `EXPECTED_CONSTRAINT` "travels, because after § D3 the
constraint IS a profile artifact" — correct, and the code that resolves it must
travel with it.

**REQUIRED CHANGE.** Name a fourth mechanical change in 4.3: the DHC lookup
resolves against the descendant's own `profile/distinct-holder-constraints/`
directory, not against `tenants/*/wallets/`. The `comparison_basis` assertion at
`:777-780` moves with it.

---

## V4 — The pin-agreement check is sited in the consumer; the ratified rule sites it in the descendant

**IMPACT: HIGH**

**EVIDENCE.** Ratified `domain-descendant-boundary`, requirement "A descendant
pins the product by commit, twice", scenario *The pin manifest and the gitlink
disagree*: "**THEN** the **descendant's own validator** REFUSES the tree rather
than preferring either, because an unanswerable question is never an implicit
pass."

The packet puts that check in LedgerxFactory. `tasks.md:182-190` (5.4): the
DELEGATING entry in LedgerxFactory "read[s] and compare[s] the THREE pin
declarations (D7) and refuse[s] on disagreement". `design.md:316-318`: "The
delegating bar entry (§ D4) reads all three and REFUSES on any disagreement".
The packet's own restatement of the scenario (`spec.md:28-31`) drops the actor:
"**THEN** the tree is REFUSED" — no refuser named.

Two consequences, both buildability. (a) A standalone `LedgerxWallet` clone has
no pin-agreement check at all — and the packet stands a ruleset up over that
repository (`tasks.md:100-101`, `:220-221`, "Promote the LedgerxWallet ruleset to
ACTIVE once a check has reported once"), so the repository is gated on a check
that does not exist. (b) D4's stated invariant is self-contradictory: 5.4 says
the delegator "holds NO rule, NO threshold" in the same sentence that gives it
the three-way comparison, which is a rule and is the only place it lives.

**REQUIRED CHANGE.** The gitlink-vs-manifest comparison (declarations 1 and 2 of
D7) moves INTO `LedgerxWallet/tests/validate_wallet_estate.py`, which is the
descendant's own validator and the artifact the ratified scenario names. Only the
third declaration — LedgerxFactory's `stack.yaml` `openxwallet.contract_ref` —
is the consumer's to compare, and that is the one thing the delegator legitimately
holds. Then D4's "holds no rule" becomes true, and the descendant refuses its own
tree without needing a consumer above it.

---

## V5 — Nothing compares any CHECKOUT to the gitlink that governs it, so a green run against unpinned contracts survives the change

**IMPACT: HIGH**

**EVIDENCE.** All three D7 declarations are RECORDED values
(`design.md:305-307`: a gitlink, a YAML `revision`, a YAML `contract_ref`). What
actually gets executed is a WORKING-TREE file: `:270`
`cmd = [sys.executable, VALIDATOR, target] + …`, with `VALIDATOR` after D5 being
the on-disk `openXwallet/scripts/validate-openxwallet.py`, and `:272`
`cwd=os.path.dirname(os.path.dirname(VALIDATOR))`. A submodule checkout sitting
at a commit other than the gitlink records — the ordinary result of a branch
switch without `git submodule update` — makes all three declarations agree while
the validator that runs comes from a commit nothing pins. The same hole exists one
level up: the delegator reads LedgerxWallet's pin file and gitlink out of
whatever LedgerxWallet checkout is present, which may not be the commit
LedgerxFactory's own gitlink records.

That is verbatim the failure the change exists to remove. The validator's surviving
comment states it as the governing hazard (`:56-63`): *"Resolving that one instead
would validate our estate against an unpinned contract version while the bar
reported green, and a silent pass is worse than a loud failure."* And the ratified
fork scenario answers it with digests — "**THEN** the descendant is a fork, the
copy is refused, and the **pin's digests** are what detect it" — while D1
(`design.md:100-106`) deliberately declines a digest block and `spec.md:100-102`
rewrites the detector as "the pin's recorded commit". A recorded commit detects
nothing unless something compares it to a checkout, and the packet builds no such
comparison anywhere.

**CONSTRAINT TO CARRY.** The invariant is FIVE reads, not three. Add, and prove
RED: (i) `git -C LedgerxWallet rev-parse HEAD` equals LedgerxFactory's recorded
`LedgerxWallet` gitlink; (ii) `git -C LedgerxWallet/openXwallet rev-parse HEAD`
equals both the pin manifest `revision` and LedgerxWallet's recorded `openXwallet`
gitlink; (iii) `git -C LedgerxWallet/openXwallet status --porcelain` is empty, so
an edited copy of pinned content refuses. Without (iii) the ratified fork
scenario has no realization at all in this packet, and D1's rejection of digests
is only defensible once (iii) exists.

---

## V6 — 4.3(a) deletes a probe corpus while 4.3 promises none is deleted, and that corpus is the PARENT's realization evidence

**IMPACT: MEDIUM**

**EVIDENCE.** `tasks.md:144-145`: "`EXPECTED_CONSTRAINT`, `ENVIRONMENT_EVIDENCING`,
`PLATFORM_VERIFIABLE`, `PIN_VERDICTS` and every negative-probe corpus are
BYTE-UNCHANGED." Deleting `VALIDATOR_CANDIDATES` and the walk (4.3(a)) necessarily
deletes, in the same act: `_NESTED`/`_AGGREGATION`/`_LEGACY` (`:284-289`), the
eight `FINDER_PROBES` (`:304-331`), `_finder_scratch()` (`:334-349`),
`check_finder_candidates()` (`:352-374`) — whose first assertion is
`if declared != [_NESTED, _AGGREGATION]` — and the `main()` call at `:804`. That
is ~90 lines of negative-probe corpus, so the claim is false as written.

It also has a governance edge. Those probes ARE the landed realization evidence of
the ratified parent. The file says so three times: `:50-52` ("Ratified design D9 of
the openxFactory change split-openxwallet-repo … realized here as its tasks.md
2.1-2.3"), `:275-276`, and `:307-313` ("INVERTED at P5b (tasks.md 10.1) … that
inversion is the whole of what 10.1 changes observably"). `split-openxwallet-repo`
archives only on merged plus green realization evidence
(`proposal.md:333-340`), so P6 deletes the parent's evidence before the parent
archives.

`check_finder_loud_failure()` (`:377-401`) can survive — it copies the module to
`<td>/tests/` (a two-level layout the destination preserves) and asserts
`"failure, not a skip"` from `main()`'s `:801-802` — but only if the new
resolution stays module-relative AND that refusal still fires FIRST, ahead of
4.3a's three new estate-root refusals. The packet states no precedence.

**REQUIRED CHANGE.** Correct 4.3's byte-unchanged claim to exclude the finder
probes; add a task recording that the parent's 2.1-2.3/10.1 evidence is
superseded by 6.6's replacement probe (and say so in the parent's realization
record, not only here); and state the refusal PRECEDENCE in `main()` so
`check_finder_loud_failure`'s asserted string is still the one that appears.

---

## V7 — The cross-tenant profile validator keeps a one-tenant path literal, and the refusal predicate is a different expression from the scan target

**IMPACT: MEDIUM**

**EVIDENCE.** `tests/validate_wallet_estate.py:39`:
`WALLET_DIR = os.path.join(REPO, "tenants", "ledgerxcorp", "wallets")` — the
tenant name is a literal. `design.md:224-226` states the refusal over a GLOB:
"REFUSES with a named exit when that root holds no `tenants/*/wallets/`
directory", and `spec.md:123` repeats it. Those are different predicates: a root
with `tenants/othertenant/wallets/` satisfies the glob, then `WALLET_DIR` misses
and the run errs at `:733` with a message naming a tenant the operator never
mentioned. D6 removes one tenant's IDS from the profile (`design.md:286-291`) and
leaves one tenant's PATH in it — the same inversion, one line up.

**REQUIRED CHANGE.** The estate manifest of §5.3 declares the tenant path (or the
tenant id) alongside the expected ids, and `WALLET_DIR` is derived from it. One
predicate, declared once, in the estate that owns the tenant.

---

## V8 — Three line citations are wrong, in tasks that are same-commit edits to a prepared live window

**IMPACT: MEDIUM**

**EVIDENCE.**

1. `models/protected-surface.yaml`: the packet says `:438` in four places
   (`proposal.md:111`, `:400`; `tasks.md:214-215`; `design.md:398-399`). The
   actual line is **455** — `git show origin/main:models/protected-surface.yaml |
   grep -n validate_wallet_estate` → `455:      RED-proven by
   validate_wallet_estate.py's`. The file is 781 lines; `grep -c` = 1, so "once"
   is right and only the number is wrong.
2. `specs/016-posting-segregation-of-duties/quickstart.md:15` (`tasks.md:199`,
   `proposal.md` § 2b): line 15 is the opening ` ```sh `. The relative validator
   invocation is at **line 19**: `python3
   ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`.
3. `tasks.md:148` cites "the `err()` at `:706`" for the estate-directory refusal.
   `:706` is inside `check_pin_reconciliation` (`capture_output=True, text=True)`
   closing the emitter subprocess at `:704-706`); the estate `err()` is at
   **:733**, `err(f"missing estate directory tenants/ledgerxcorp/wallets")`.

**REQUIRED CHANGE.** Fix all three before realization. This is not pedantry:
5.6 is THE LIVE-WINDOW GUARD, performed in the same commit as the move, on a
runsheet whose operator mints real keys — an implementer following `quickstart.md:15`
edits a code fence.

---

## V9 — The quickstart edit is not "a link change only"; it is the direct-integration path the packet's own spec forbids

**IMPACT: MEDIUM**

**EVIDENCE.** `specs/016-posting-segregation-of-duties/quickstart.md:17-19`:

```sh
for f in tests/validate_*.py; do python3 "$f" || break; done
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict
```

`design.md:341-344` (D9): "The repoint is a LINK change only. No step, actor,
abort condition or evidence requirement is touched." The runsheet reference at
`:23` is indeed a link. This one is a COMMAND, and the command resolves the
product's validator through openxFactory's nested gitlink — precisely
`spec.md:59-61`'s refused shape: "**WHEN** a LedgerxFactory tool resolves the
openXwallet validator at a path outside `LedgerxWallet/openXwallet/`, such as a
parent directory's `openxFactory/openXwallet/` … **THEN** the resolution is a
direct integration of the product and is refused."

**REQUIRED CHANGE.** Split 5.6 into the link repoint (`runsheet.md:23`) and the
BAR repoint (`quickstart.md:19` → `LedgerxWallet/openXwallet/scripts/validate-openxwallet.py`),
and drop "links only" from D9 for the second. It is also the strongest available
conformance evidence for requirement 2, so it is worth stating as such rather
than as bookkeeping.

---

## V10 — Task 5.8 fixes nothing measurable and, as worded, risks removing an allowlist entry that is still needed

**IMPACT: MEDIUM**

**EVIDENCE.** `KNOWN_KIND_REGISTRY` (`tests/validate_document_estate_surface.py:899`)
is used in exactly one place, as a MEMBERSHIP test on a file that is scanned
(`:1340-1344`):

```python
elif doc["kind"] not in KNOWN_KIND_REGISTRY:
    err(f"{rel}: kind {doc['kind']!r} is not a member of the "
        f"closed {len(KNOWN_KIND_REGISTRY)}-item kind registry (CHK002)")
```

There is no bijection or unused-entry check. The only anti-rot in that file is
`check_warrant_declaration()` (`:1222-1254`), and it runs over the WARRANT's
`owned_paths`, not the registry: "every declared path must resolve to at least
one real file". And `specs/001-document-estate-read/warrant.yaml` does not own
the wallet paths — its `templates/` entries are `templates/document-*.yaml`,
`templates/fact-*.yaml`, `templates/disclosed-gap-record.yaml`,
`templates/discovery-closure-record.yaml`, `templates/steady-state-manifest.yaml`,
and there is no `tenants/*/wallets/**` or `tests/validate_wallet_estate.py` entry.

So: when the template leaves the tree the validator **silently passes**, the
registration is already inert today, and `proposal.md`'s Impact claim that "the
surrounding entries show that file treats its registrations as load-bearing" is
an overclaim. 5.8 is also asymmetric — the DHC also stops having an in-tree
artifact, and `xfactory_wallet_distinct_holder_constraint` must STAY registered
so a future estate DHC does not red.

**REQUIRED CHANGE.** Re-word 5.8 as a dated NOTE beside the retained entry
recording where the artifact went (which is what the surrounding style actually
is), not a deregistration; and state in the packet that the registration is an
allowlist with no unused-entry check, so nobody later reads 5.8 as having closed
a gate.

---

## V11 — The estate manifest has no path, no `kind:` and no `schema_version`, and it lands in an unpinned directory

**IMPACT: MEDIUM**

**EVIDENCE.** `tasks.md:180-181` (5.3) is the whole specification: "Write the
estate manifest (D6) beside the records it enumerates: the two wallet ids and the
two grant→wallet bindings, declared as data." D6 (`design.md:286-291`) adds no
path, kind or schema. Three concrete consequences:

- Every YAML in this corpus carries `schema_version` + `kind` (house rule; and
  `validate_document_estate_surface.py:1338-1341` errs on either missing where it
  scans). Neither is named.
- "Beside the records" means `tenants/ledgerxcorp/wallets/`, which the upstream
  sweep reads. If the manifest were given a wallet-family kind it would be
  adjudicated as a LIVE RECORD (`validate-openxwallet.py:2102-2104`) and would
  also move the V1 count. The packet must state that its kind is deliberately
  NOT a wallet-family kind.
- `tenants/` is not a protected directory — `models/protected-surface.yaml`'s
  `protected_directories` are exactly `credentials`, `adapters`, `policies`,
  `openspec/specs`, `conformance` — so the manifest is unpinned data. The
  authority for "which wallet ids are expected" therefore moves OUT of a `tests/`
  file the bar's own glob covers and INTO unpinned data no digest guards. D6's
  "STRICTLY stronger" is true for shape (it catches a record added without a
  declaration) and weaker for authority (a record plus a matching declaration
  now passes with no gate).

**REQUIRED CHANGE.** Name the path, the `kind:`, and whether anything validates
its shape. If nothing does, say so — and consider a digest row, since
`models/protected-surface.yaml` is the mechanism this repository already uses for
exactly this problem.

---

## V12 — Task 4.5 creates the second truth D4's own testable property forbids

**IMPACT: MEDIUM**

**EVIDENCE.** `tests/validate_wallet_estate.py:142`
`ENVIRONMENT_EVIDENCING = {"holder_readable", "isolated_invocable"}` is enforced
at `:751-755`. `tasks.md:144` declares it BYTE-UNCHANGED. `tasks.md:161-167`
(4.4/4.5) adds `profile/custody-posture.yaml` declaring the same posture
(`holder_readable`, environment-evidencing, ceiling `act`) and has the validator
check the records against it. The posture then exists in two places — a literal
set in code and a declared artifact — which is exactly what D4's stated property
forbids (`design.md:200-202`): "**every rule, threshold, expected set and probe
corpus appears in exactly one file**". 4.6's grep-based proof, honestly run, fails
on this pair.

**REQUIRED CHANGE.** If 4.4 lands, `ENVIRONMENT_EVIDENCING` and the `act` ceiling
literal at `:770-773` are READ FROM the posture file and stop being
byte-unchanged — say so in 4.3. If 4.4 is cut to a successor (D8 says it can be,
in one line), 4.5 goes with it and nothing else moves. Those are the only two
coherent options; the packet currently specifies a third that 4.6 would red.

---

## V13 — The moved validator leaves the discoverability scan, and that is a real if small coverage loss

**IMPACT: LOW**

**EVIDENCE.** `tests/validate_protected_surface.py:179-189` reads sources only
from its own directory:

```python
for fn in sorted(os.listdir(HERE)):
    if not (fn.startswith("validate_") and fn.endswith(".py")):
        continue
```

with `HERE = os.path.dirname(os.path.abspath(__file__))` (`:44`), and applies
`ENFORCEMENT_PATTERN = re.compile(r'for\s+\w+\s+in\s+\((\s*"[^"]+"\s*,[^)]*)\)')`
(`:122-123`) to enforce "No validator may enforce a protected directory that the
declaration does not name". After the move, `LedgerxWallet/tests/validate_wallet_estate.py`
is outside that scan permanently. Today's file trips nothing (its loops iterate
NAMES — `for parts in VALIDATOR_CANDIDATES`, `for name, code, files in PROBES` —
never a literal tuple), so this is a future-coverage loss rather than a present
break. The delegator must likewise avoid a literal `for x in ("a", "b", …)`
naming two or more protected directories.

**CONSTRAINT TO CARRY.** Record the loss in D2's price paragraph beside the
notebook/ideation price it already names, so it reads as a decision. It needs no
task.

---

## V14 — `.gitmodules` mechanics are safe in CI, and the loud refusal becomes the DEFAULT state in most automated checkouts

**IMPACT: LOW**

**EVIDENCE.** The parent's app-token/`insteadOf` problem does NOT reappear here.
openxFactory `.github/workflows/doc-health-reusable.yml:156-158` (and the
identical `:904-906`):

```sh
SUBS=$(git config --file .gitmodules --get-regexp 'submodule\..*\.path' \
       | awk '{print $2}' | grep -E '^(openxFactory|xFactories/)')
git submodule update --init $SUBS
```

That matches `xFactories/LedgerxFactory` and is explicitly non-recursive (`:163-165`:
"NOT `--recursive`, which would additionally pull `installs/omnigent-install`
and every domain's nested submodules into every aggregation doc-health run"), so
`xFactories/LedgerxFactory/LedgerxWallet` is never initialized in CI and no token
ever needs to reach it. LedgerxFactory itself has no workflow to break —
`git ls-tree -r origin/main` under `.github/` returns exactly `CODEOWNERS` and
`copilot-instructions.md`. And a recursive aggregation clone already requires SSH,
because `.gitmodules` on `origin/main` today is
`[submodule "ledgerXavatar"] url = git@github.com:opensoft/LedgerxAvatar.git` —
so 5.1's SSH URL adds a second instance of an existing requirement, not a new
class of failure.

The consequence worth carrying: because CI and most fresh clones will NOT have
`LedgerxWallet` initialized, the delegator's refusal is the DEFAULT state rather
than an exceptional one. The fail-closed design is right, and it means the wallet
estate's coverage now rests entirely on a human running the glob in a checkout
where the submodule happens to be initialized.

**CONSTRAINT TO CARRY.** State it in D4 beside "quieter than a CI break, not
safer" — after this change the bar's wallet leg is one un-run
`git submodule update --init` away from refusing everywhere, which strengthens
the case for the CI successor `tasks.md:259-261` already names.

---

## What I checked and found sound

- **The pin-checker leg — my primary suspicion — is now covered.** `design.md:228-264`
  and `tasks.md:146-158` (4.3a) enumerate all three of the legs I independently
  found in the source: the `stack.yaml` read at `:675-676`
  (`yaml.safe_load(fh)["xfactory"]["contract_ref"]` — note it is the openxFactory
  BUNDLE pin, not the openXwallet one, which the packet correctly distinguishes),
  the second five-level walk `find_aggregation()` at `:583-595`, and the pinned-emitter
  extraction at `:687-689` / invocation at `:704-706` passing `REPO` as the
  consumer root. The decision to START the second walk from the estate root rather
  than from the module (so nesting does not spend one of five levels, and a
  LedgerxWallet worktree two) is the correct call and is not obvious. 4.3b's
  explicit PyYAML declaration is right — every validator in this repo does
  `import yaml` (`validate_protected_surface.py:42`,
  `validate_document_estate_surface.py:85`), so the dependency is real and is
  currently inherited rather than declared.
- **`models/protected-surface.yaml` owes no digest re-pin.** Verified directly:
  no `- path:` row matches any of the three moved paths, and the five
  `protected_directories` (`credentials`, `adapters`, `policies`, `openspec/specs`,
  `conformance`) contain none of them, so `admission_findings`'s
  `os.walk(root)` over declared directories (`:113-118`) cannot see the move.
  Corroborated by the repo's own prior finding at
  `specs/018-openxwallet-pin-bump/evidence/suite-baseline-vs-after.txt:74`:
  "`tests/validate_wallet_estate.py` is NOT a pinned file and `tests/` is not"
  a protected directory. Only the line number is wrong (V8).
- **`docs/protected-surface.md:62` tolerates a script that needs a submodule.**
  The bar is `for f in tests/validate_*.py; do python3 "$f" || echo "FAIL $f"; done`
  — exit-code only, no import, no environment assumption. A delegator that shells
  out and propagates its child's code satisfies it exactly, and keeping the PATH
  is genuinely the load-bearing choice.
- **`constraint_id` survives the move by ID.** `runsheet.md:174` references the
  DHC by id, not by path, so 4.2's claim holds and no edit is owed there.
- **The annotated-tag dereference is real and correctly handled.** D1 and 3.4
  resolve `wallet-v1.1^{commit}`; the tag object is `021cdeef…` and the commit
  `63f5a1ad…`, which is what `stack.yaml:55` already declares. Writing a tag id
  into a `revision_kind: commit` field is a genuine trap and the packet names it.
- **The MedxChart-not-MedxAvatar pin shape is the correct reading of the ratified
  rule**, which settles the shape "FORWARD only" and says it "SHALL NOT be read as
  retro-fitting them". D1's rejection of a digest block is defensible as written —
  but only once V5's checkout-vs-gitlink comparison exists to replace what digests
  were doing in the ratified fork scenario.
- **Nested-only placement is the ratified placement**, and D2 names its
  governance-visibility price rather than hiding it. Correct on the corpus:
  openxFactory's enumerations key on `xFactories/<Name>`.
- **Q2's disposition is right on the evidence.** The four estate records carry
  holder ids, DIDs, key ids and a live `state:`; the DHC names none of those. The
  profile/instance test in D3, and D3a's single named seam exception, are the
  right shape for a first-of-standard packet — a list of three files would not
  have travelled to the next descendant.
