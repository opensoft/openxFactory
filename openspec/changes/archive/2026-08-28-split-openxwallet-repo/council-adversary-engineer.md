Reviewer role: Adversary Engineer (council review, read-only) — 2026-08-26
Subject proposal: openspec/changes/split-openxwallet-repo/proposal.md

# Adversary Engineer — `split-openxwallet-repo`

Five concerns plus one lead-security limb. Each is stated as the attack, not as
the tidiness complaint, because the question I am asked is what a motivated
candidate does with this boundary the week after it lands.

---

## Concern 1 — The deprecation minor as drafted breaks the byte-identity floor and reds the only consumer (HIGH, raised jointly with the Systems Architect's #1)

**Attack.** Nothing adversarial is needed: P2.5 as drafted self-inflicts. Making
`scripts/validate-openxwallet.py` emit a deprecation warning edits the validator
inside a move whose only safety property is an empty diff, and it reds
LedgerxFactory's `--strict` estate run (`tests/validate_wallet_estate.py:196-205`
against `scripts/validate-openxwallet.py:2107`) while being surfaced by no
required check, since openxFactory's own gate runs without `--strict`
(`.github/workflows/wallet-validation.yml:34`).

**Verdict — VALID, HIGH.** Manifest-carried `relocating:` marker; the validator
is not edited in openxFactory by P2.5; the conformance-validator clause
discharged by naming the pinned openXwallet validator; all proofs restated
against a NAMED CARVE COMMIT.

**Disposition — APPLIED.** See `council-systems-architect.md` § Concern 1 for the
full applied text; P2.5, § Out of scope's tail, the byte-identity floor,
`code_surface` and the P2.5 evidence row all changed.

---

## Concern 2 — After P3, a candidate can repoint its own checker and clear the result by council (HIGH)

**Attack.** The floor protects the register FILE. It does not protect the pin or
the gitlink that determine WHICH READER opens that file. So: one pull request
that bumps the `openXwallet` gitlink to a checkout with a neutered
`check_register` AND edits a grant under `governance/review-authority/`. It
matches no floor path, so it is council-clearable, and the check that would have
caught it is the one being replaced by the same pull request.

**Evidence.** codexFactory
`scripts/merge_master/openxfactory-review-authority-floor.yaml` lists exactly ONE
`never_clearable_paths` entry, `governance/review-authority/register.yaml`, and
`repository_floor.py::matching_paths` is exact set membership
(`path in protected`). Nothing covers `contracts/openxwallet-pin.yaml` or
`openXwallet`. `_parse_exact_path` rejects a leading or trailing `/` and accepts
the bare gitlink name, so the fix is expressible in the existing schema.

**Verdict — VALID, HIGH. "codexFactory — NO change" is REVERSED.** A required
successor **P3b — codexFactory floor widening**, landing in P3's wave, adding
`contracts/openxwallet-pin.yaml` and `openXwallet` (gitlink form, no trailing
slash) with its own realization-evidence row. `neutral-product-pin` carries the
general rule as a scenario.

**Disposition — APPLIED.** P3b added as an AUTHORIZES bullet with the attack
spelled out; the § "The register stays" section reversed ("**codexFactory DOES
need a change, and this reverses an earlier claim in this proposal that it did
not**"); ## Impact's codexFactory bullet rewritten from "NO change" to "ONE
required change, P3b"; § Out of scope's "or any change to codexFactory"
explicitly WITHDRAWN; `code_surface` raised from five repositories to SIX;
`neutral-product-pin` gains the scenario "WHEN one pull request changes the
product pin or its gitlink AND any file under the review-authority register's
directory THEN the pull request is human-only".

**Recorded, and explicitly NOT this change's scope:** the same floor file omits
`governance/review-authority/{grants,wallets,attestations}/`, so a grant, wallet
or attestation file is editable outside the floor today, with only the register
index protected. That is a PRE-EXISTING finding for the owner of
`add-wallet-carried-review-authority`, which created those directories. Recorded
under ## Impact and in § Out of scope.

---

## Concern 3 — Task 2.6's red-proof is sent to a repository with no register, and the check can pass vacuously (HIGH)

**Attack.** Two ways to end up with a green REQUIRED check that verified nothing.
First, the proposal sends 2.6's red-proof to openXwallet — whose tree has no
`governance/review-authority/` at all, so whatever turns red there is not the
control. Second, `main()` runs `repo_scan` — and therefore `check_register` —
only `if args.path is not None` (`scripts/validate-openxwallet.py:2160`). Point
the pinned validator at `openXwallet`, or omit the argument, and it self-tests
and exits 0. `grep -rn "wallet-validation.yml" tests/` returns nothing, so
nothing in the repository currently pins the invocation.

**Evidence.** `add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:30-33`
confers authority only where the reader "runs as a REQUIRED check on the
repository that holds the register". R6 keeps the register in openxFactory.

**Verdict — VALID, HIGH.** Move 2.6's red-proof to openxFactory, retargeted at
the consumer gate; add an evidence row proving the reader RAN; add a
`neutral-product-pin` scenario refusing a target-less invocation; pin the exact
invocation string in a test.

**Disposition — APPLIED.** § "The REQUIRED check" now says the red-proof
"discharges in openxFactory, retargeted at the consumer gate — not in the new
repository", with the spec citation and the reason (openXwallet has no
`governance/review-authority/` for a malformed row to sit in). A dedicated
evidence row: "the consumer gate's log line naming
`governance/review-authority/register.yaml` as READ, plus the task-2.6 red-proof
run id — a green check whose log never names the register is a vacuous pass." P3
gains the pinned-invocation test obligation with the `:2160` citation.
`neutral-product-pin` gains "WHEN a required check invokes a pinned validator
without a scan target THEN the check REFUSES rather than self-tests".

---

## Concern 4 — The vendored envelope schema is checked for PRESENCE, not identity (MEDIUM-HIGH)

**Attack.** Rule (g) reads the approval-scope vocabulary out of the vendored
`hermes-job-envelope.schema.yaml`. Edit that vendored file in openXwallet and the
vocabulary the gate enforces changes — and nothing notices, because `main()`
checks only `ENVELOPE_SCHEMA_PATH.is_file()`
(`scripts/validate-openxwallet.py:2124`). The pin exists on paper; the read does
not consult it.

**Evidence.** openAvatar's `contract_pin.yaml:15-21` documents the house
fail-closed shape — a named `verify_pin` where "a recomputed digest can never
equal an empty recorded digest → drift → fail before any test". openXwallet's
`contract_pin.yaml` was given no verifier. And
`shared-contract-ownership:142` requires all publisher markers together, which
raises the separate question of how openXwallet's own manifest treats a file it
does not own.

**Verdict — VALID, MEDIUM-HIGH.** `neutral-product-pin` states the rule; the
`wallet-validation` job gains an explicit verify step with its own evidence row;
openXwallet's `contracts/manifest.yaml` registers the vendored file as a CONSUMED
member so the `:142` marker test is met without claiming ownership.

**Disposition — APPLIED.** `neutral-product-pin` gains "a vendored foreign
contract SHALL be digest-verified against the repository's `contract_pin.yaml`
before it is read, and an unverifiable copy refuses the run", with the `:2124`
and openAvatar citations. P2 requirement (iii) is the verify step plus the
CONSUMED-member manifest row (`compatibility: canonical_openxfactory_contract`,
`adapter_owner: openxFactory`, digest = the pinned openxFactory row's). New
evidence row: the verify log line plus a RED run with a mutated copy.

---

## Concern 5 — The wave has no runbook, the new repository's ruleset cannot be REQUIRED on day one, and two hidden clocks can strand it (MEDIUM, raised jointly with the Product Advocate's #1)

**Attack.** A multi-repository carve with an atomic breaking merge in the middle,
run from prose. Three concrete failure modes: a case-variant repository name
already held in the org or a fork (GitHub names are case-insensitive-unique) kills
the carve after it is taken; the new repository's ruleset cannot be ACTIVE before
the check has reported once, so "required from day one" is not achievable; and a
declared freeze on `contracts/manifest.yaml` across P2.5 → P3 is unenforceable in
a shared checkout across sessions, so the eight digests P2 proved are not
necessarily the eight digests P3 merges against.

**Evidence, and the clock the proposal does not mention.**
`governance/review-authority/register.yaml:37` carries
`expires_at: "2026-11-23T12:00:00Z"`, and `check_register` raises
`register-row-expired` as an **error** once that instant passes
(`scripts/validate-openxwallet.py:1961-1965`) — which reds the REQUIRED gate on
every pull request thereafter, including the wave's own.

**Verdict — VALID, MEDIUM.** Add `docs/openxwallet-cutover-runbook.md` to P2's
scaffold as a code surface, ordered and reversible; add the register-expiry
sequencing constraint; add the rebase-and-re-verify constraint.

**Disposition — APPLIED.** `docs/openxwallet-cutover-runbook.md` added to
`code_surface` (1) and to P2's AUTHORIZES bullet, with a new § "The cutover
runbook, and it is P2's own artifact" enumerating all six ordered phases: the
case-variant name check BEFORE the carve; the carve with a completeness check
naming `specs/006-openxwallet-contracts/evidence/` and
`contracts/openxwallet/examples/negative/` explicitly; CODEOWNERS; the ruleset in
EVALUATE mode → one trivial pull request so `wallet-validation` reports and
becomes selectable → promote to ACTIVE, with "day-one REQUIRED is impossible"
stated; the `wallet-v1.0` tag after byte-identity; submodule init in openxFactory
and the aggregation with byte-identity re-proved from each; and rollback per
phase. Sequencing item 8 carries the expiry clock with the ruling "either the row
is re-issued before 2026-11-23, or **P3 is not scheduled after 2026-11-01**";
item 9 carries "the declared manifest freeze is UNENFORCEABLE, so P3 REBASES and
RE-VERIFIES the eight digests immediately before merge". The openXwallet ruleset
evidence row now records "required from day one" as unachievable and replaces it
with the bootstrap sequence.

---

## LS-A3 (lead-security limb, folded into the Systems Architect's #3) — the sweep walks into the submodule and the carve can re-adjudicate the negative corpus

**Attack.** Two silent-inversion paths in the consumer gate. The sweep walks INTO
`openXwallet/` — a submodule's `.git` is a FILE, so the existing `.git` skip does
not fire — and `repo_scan`'s corpus exclusion keys on `"examples" in path.parts`
plus an `openxwallet*` part (`scripts/validate-openxwallet.py:2050-2053`), so a
carve that flattens or renames those prefixes causes the 36 intended-invalid
negatives to be re-adjudicated as LIVE records inside a REQUIRED check.

**Verdict — VALID, MEDIUM.** Both applied: P2 requirement (ii) preserves the
`contracts/openxwallet*/examples/` prefixes as an acceptance line, and P3 carries
the sweep exclusion with the mechanism left to design (N4).

**Disposition — APPLIED.** See `council-systems-architect.md` § Concern 3.

---

**DISMISSED: none.** Every concern I raised survived the lead's check against the
tree. What I did NOT find: any weakening of a gate by the pin direction itself,
any bypass created by the atomic P3, or any path by which the byte-identity floor
is optional. The boundary is defensible; five of the six ways it was going to be
built were not.
