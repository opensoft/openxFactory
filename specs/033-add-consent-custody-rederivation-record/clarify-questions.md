# Clarify questions — 033-add-consent-custody-rederivation-record

**Round 1 (STOP A), 2026-09-09, lane `opsXfactory-1`.** Twelve questions. The
reused F.3 rulings (Q1 tick-with-evidence and the `3b530009` amendment form, Q4
dual evidence, Q5 same-commit, Q9 full Speckit tree, Q10 frozen ratified prose)
are taken as settled and are NOT re-asked. Everything below is something they do
not settle, each stated with what was MEASURED on branch
`033-add-consent-custody-rederivation-record` (base `main` `6df21737`).

---

## Q1 — `contract-v3.5` is free. How do § 5.2–5.5 land when the merge IS the cut?

**Measured.** `contracts/manifest.yaml:3` declares `contract-v3.4`;
`contracts/releases/` holds `contract-v3.4.digests.yaml` as its highest (283
entries); `git tag -l 'contract-v*'` tops out at an annotated `contract-v3.4`.
No surface carries `contract-v3.5`. `contract-v2.6` is the SPENT number, not
this one. **The next additive minor is `contract-v3.5`** — a measurement, and
§ 5.1's claim on issue #630 row 4 is the LANE's to post, not mine.

**Measured precedent.** `contract-v3.4` was cut by PR #653 and landed as a
SQUASH commit `807a4f47` (one parent, committer GitHub, subject `… (#653)`) —
so the landed commit is NOT the reviewed candidate, and
`docs/contract-versioning-policy.md` § *Bundle Realization Order* step 4 says
the landed commit then "becomes the new candidate and every gate and review
reruns before tagging."

**Ask.** (a) ONE pull request carrying §§ 2–5 together, or TWO (the growth
first, the cut second on a re-measured number)? (b) Given the squash, is § 5.5
ticked on the pre-merge gate evidence at the exact candidate, with the post-merge
re-run recorded as OWED to whoever lands it — or is § 5.5 a NOT-OWED for me
because I neither merge nor land?

---

## Q2 — WITHHELD needs an exit-status class, and this repository has ruled none

**Measured.** Every `Exit codes:` docstring in `scripts/` reads `0 ok, 1
findings, 2 harness error`. The only `3` in the tree is
`scripts/avatar-metering-alert.py` — "nothing crossed a paging threshold" —
which is a different meaning. `Findings` in
`scripts/validate-consent-instruments.py` carries `errors` / `warnings` /
`notes` and nothing else. Task 3.4b asks for "the one the repository rules for
'needs a human decision'". **There is no such rule to read.**

**HARD CONSTRAINT, measured.** § 4.8c puts a WITHHELD fixture INSIDE the
packaged corpus, and the packaged self-test runs on every invocation. So
whatever class is chosen, `python3 scripts/validate-consent-instruments.py
--strict` with no path argument MUST still exit 0 over the packaged corpus, or
this feature reddens every caller — the same failure mode
`validate-release-tag-gate.py`'s own header records for `release-tag-publication`
in September.

**Ask.** Which:

- **(a)** a new exit code `3` for a REAL instrument that withholds, with the
  packaged self-test's withheld fixture explicitly not raising it (the fixture
  is an *expected* withholding, like a negative is an expected failure);
- **(b)** exit `0` always, WITHHELD carried only in the report line and the
  named outcome, leaving the exit-status escalation to the consumer's gate;
- **(c)** exit `3` unconditionally, and CI callers are changed to tolerate it;
- **(d)** something else you name.

If (a) or (c), name the code — I will not invent an exit-status vocabulary for
this repository.

---

## Q3 — Where does the withheld fixture live, and how does `self_test` hold a third bucket?

**Measured.** `self_test` has exactly two loops: `EXAMPLES_DIR.glob("*.example.yaml")`
(must validate cleanly, else `expected a valid example`) and
`NEGATIVE_DIR.glob("*.yaml")` against `EXPECTED_NEGATIVE_FINDINGS` (must fail
for a declared code, with fail-closed both ways for unregistered/missing files).
A withheld fixture in either loop breaks it. The corpus today is **6 valid + 7
negative + 2 purpose probes**.

**Ask.** (a) A THIRD directory `examples/consent-instrument/withheld/` with an
`EXPECTED_WITHHELD_OUTCOMES` table mirroring the negatives' fail-closed
discipline — or the fixture kept among the positives with an opt-out set? (b)
Does layer 2 (`repo_scan`, real artifacts under a path argument) need the same
third bucket, or does it simply report WITHHELD as it finds it?

---

## Q4 — Do any schema identity fields other than `contract_schema_version` move?

**Measured.** The file carries `$schema` (draft 2020-12), `$id:
"consent-instrument.schema.yaml"`, `contract_schema_version: 2`, and the record
property `schema_version: const: 1`. The `contract-v1.33` precedent
(`add-client-identity-roster`, `1 -> 2`) moved `contract_schema_version` ONLY —
`$id` unchanged, `const: 1` unchanged, and the manifest row's own
`schema_version: 1` field unchanged.

**Ask.** Confirm the same here: `contract_schema_version` `2 → 3` and NOTHING
else — `$id` frozen, the record envelope's `const: 1` frozen, and the
`contracts/manifest.yaml` `consent-instrument` row's `schema_version: 1` frozen.

---

## Q5 — When does the manifest's `consent-instrument` digest move?

**Measured, and it forces half the answer.** The row pins `sha256:
13b0fe46fdb8791020b426dcd763aced2a3280a82923b32d3a0d0877ab6ad441`, and
`sha256sum` over the file returns exactly that. `python3
scripts/validate-manifest-digests.py` verifies **189 per-file digests** and is
run inside `pytest-suite` by `tests/manifest_digests/test_manifest_digest_sweep.py`.
So the moment the schema file changes, the digest is stale and the REQUIRED
pytest gate is red until it is re-derived. It cannot wait for § 5.2.

**Measured, second leg.** `contracts/schemas/consent-instrument.schema.yaml` is
**NOT** a member of the release digest inventory —
`contract-v3.4.digests.yaml` carries five `contracts/schemas/*` paths and this
is not one of them. So the schema edit re-bases a manifest row and adds no
inventory row.

**Ask.** (a) Confirm the `sha256` re-derivation rides the § 2 schema commit
(forced by the gate above) while `contract_bundle_version` and the
`consumption_rule` prose ride the § 5.2 candidate commit — three edits to one
file across two commits. (b) The `consumption_rule` today ends with the
`contract-v1.33` paragraph; does § 5.2 APPEND a `contract-v3.5` paragraph in
that same style (what grew, that it is additive, that the envelope stayed), or
rewrite the rule? (c) Confirm `consent-instrument-class-registry`'s row is
untouched — nothing in this change reaches class declarations.

---

## Q6 — How much does the `contract-v3.5` CHANGELOG entry have to name?

**Measured.** `git diff --name-status contract-v3.4 HEAD -- contracts/` reports
**4 additions and 14 modifications**, none of them this session's: added
`openspec-cli-pin.yaml`, `openspec-cli-pin.1.12.0.package-lock.json`,
`policies/repository-identity.yaml`, `review-lane-repin-binding.template.yaml`;
modified `README.md`, `manifest.yaml`, `openreposhape-pin.yaml`,
`openxwallet-pin.yaml`, `review-lane-pin.yaml`, `review-lane-floor-snapshot.yaml`
and eight `hermes-domain-overlay` / `omnigent` example fixtures. Separately,
`2026-09-08-publish-openspec-cli-pin-as-contract-member` chose **A-defer** over
**A-cut** (`contract-v3.5` in that PR), unvetoed — so that registration is
waiting for THIS bundle to publish it.

Task 5.3 says the entry "names what changed in the bundle, not what this session
intended", and the `contract-v3.4` entry did exactly that, attributing every
moved path to its originating pull request.

**Ask.** Confirm the § 5.3 entry attributes ALL of the above by originating
change/PR — and confirm the change class is ADDITIVE (minor): one new optional
property, one `contract_schema_version` bump, no field removed, no enumeration
narrowed, every existing instrument valid unchanged.

---

## Q7 — Where do the two new tests live, and what proves the blob walk?

**Measured.** There is no `tests/consent*` directory. Sibling test packages mix
conventions: `tests/client-identity-roster` and `tests/doc-health` use hyphens;
`tests/manifest_digests`, `tests/sequenced_after`, `tests/scope_globs` use
underscores. CI runs `python3 -m pytest tests/ -q -m "not postgres"`.

**Ask.** (a) Directory name for the new package — `tests/consent_instruments/`
(underscore, importable) or `tests/consent-instruments/` (hyphen, matching the
contract family's spelling)? (b) Is task 3.5's blob-walk extension proved by the
§ 4.8b negative fixture ALONE (self-test), or does it also get a pytest? (c)
Task 3.3's no-git assertion — is a source-level assertion (no `import
subprocess`, no `git` token, no filesystem read of a locator in the module)
sufficient, or do you want a runtime assertion that patches `subprocess` and
`Path.open` and proves neither is reached?

---

## Q8 — Four README sentences this realization falsifies, and one substrate

**Measured.** `README.md` carries four statements about this packet's box count:

1. **line 856–857**, its own OpenSpec Records row: *"**all 46 boxes in
   `tasks.md` stay unticked**"* — becomes FALSE.
2. **line 2949**, inside `govern-archived-record-edits`' row: *"exactly as the
   sibling `add-consent-custody-rederivation-record` left its 46"* — past tense,
   arguably survives.
3. **line 3022**, inside the `add-pre-archive-citation-gate` narrative: *"that
   packet is a ratified PROPOSAL with all 46 boxes unticked, so the three pins
   are still broken"* — present tense, becomes FALSE (the pins DO stay broken:
   that half is § 6, the consumer's).
4. **line 3098–3100**: *"measured 2026-09-09 UTC at `main` `6cc06288`, that
   packet still carries all 46 boxes unticked"* — a DATED measurement, stays
   true as written.

**Ask.** (a) Which of 1–4 take the `3b530009` amendment form, and which are left
as true-when-written? (b) `README.md`'s OpenSpec Records block is a row-3 shared
substrate on issue #630 under Lane Collision Protocol Amendment 1 Rule 7 — does
amending an EXISTING row (adding no new one) need a fresh substrate claim from
the lane before I write, or does the change's standing row-3 claim
(`5571680388`, 2026-09-07) already cover it?

---

## Q9 — How far does `examples/consent-instrument/README.md` grow?

**Measured.** It carries `Status: draft` and four sections: a Layout tree with a
one-line annotation per file, a *Schema → example map* table, a *Named cases
from the spec* list, and *Validating locally*. This feature adds roughly 4
positives, 10 negatives and 1 withheld — nearly tripling the tree.

**Ask.** (a) Do all four sections grow (tree entries, table cells, one *Named
case* bullet per new spec scenario), or is the growth confined to the tree and
the table with ONE consolidated *Named case* covering the custody-chain family?
(b) Does the withheld bucket get its own row in the *Schema → example map*
table, which today has only "Valid example(s)" and "Negative example(s)"
columns?

---

## Q10 — Are the candidate finding codes adopted as written?

**Measured.** `tasks.md` offers them as "candidates", and the ratified delta
names no finding code at all: `custody-chain-unanchored`,
`custody-chain-broken-link`, `custody-chain-locator-gap`,
`custody-chain-out-of-order`, `custody-pin-rewritten`,
`custody-path-class-digests-differ`, `custody-content-class-withheld`.

**Ask.** Adopt all seven verbatim, or do you want different names? (Adopting
them verbatim is my recommendation — they match the file's existing
`custody-sha256-malformed` / `embedded-original-content` style and a fixture
table will pin each one, so renaming later is a corpus-wide edit.)

---

## Q11 — Is a local `release-tag-gate` run tickable evidence for § 5.4?

**Measured.** `release-tag-gate` is a GitHub workflow evaluating pull requests
that touch `contracts/manifest.yaml` or `contracts/releases/`; its logic is
`scripts/validate-release-tag-gate.py`, runnable locally with `--head` / `--base`.
I do not open pull requests, so I cannot observe the workflow.

**Ask.** Is § 5.4 ticked on the local run of all five gates against the exact
candidate (with the transcripts in `evidence/`), leaving the workflow's own
green as the lane's post-open observation — or does § 5.4 stay unticked until a
workflow run exists?

---

## Q12 — Exactly which entry fields does the extended `walk_strings` cover?

**Measured.** Today `check_custody` walks EVERY string under `custody` and skips
only `custody.sha256`, so `custody.locator` IS walked. Task 3.5 names
`ruling_ref` and `.recorded_by` as the target and adds that "the locators are
opaque POINTERS and are walked on the same footing as `custody.locator` is
today."

**Ask.** Walk the whole entry with the same two-digest skip (`previous_sha256`,
`observed_sha256`) — which also covers `commit`, `at`, `diff_class` and `reason`
harmlessly, since a pattern/enum/format already bounds each — or walk EXACTLY
the four free strings (`previous_locator`, `observed_locator`, `ruling_ref`,
`recorded_by`)? The first is the "wherever it hides" posture the guard exists
for; the second is narrower and cheaper to explain.

---

**Awaiting answers.** Nothing in §§ 2–5 is written until this round is ruled;
the branch and this specification are the only artifacts on disk.
