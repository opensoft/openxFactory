# Tasks: add-notebook-hosting-credential-custody

Status: ratified
Ratified: 2026-08-23 — `review/ratification-2026-08-23.md`. These are AUTHORIZED, not performed, by the ratification.

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
deltas and these records. **No task here creates, moves, or reads a live
secret**: putting the password into the vault is an operator's act under the
landed rule, evidenced per `credential-contracts`, and it is listed in §4 as
that operator act rather than as work this change performs.

## 1. The hosting record declares its custody

- [x] 1.1 Add a `custody:` block to `examples/notebook-projection-hosting.yaml`
  carrying a BY-REFERENCE pointer only: the BINDING'S IDENTIFIER and what the
  custody covers. NOT the `secret_ref` — that field belongs to the binding
  instance, and duplicating it here would invite the rest of the binding to
  follow (review note, 2026-08-23). No password, recovery code, TOTP seed,
  session cookie, or exported profile — in this file or any other.
- [x] 1.2 State the custody's honest reach in the record itself: which secrets
  the binding holds, and that the sign-in's interactive step remains. A
  reference that implies unattended access invites a reader to plan on it.
- [x] 1.3 Leave `self_hosted` declarations free of the obligation, matching the
  two-case model: no operator, no obligation.

## 2. The validator enforces by-reference-only

- [x] 2.1 Teach `scripts/validate-notebook-projection-hosting.py` the custody
  rule: an operator-hosted declaration carries a custody BINDING IDENTIFIER; a
  self-hosted one need not. Refuse a `secret_ref` in the hosting record too —
  it is binding detail, and the record's job is to point at the binding.
- [x] 2.2 REFUSE anything secret-shaped in the record — a `password`,
  `totp`/`otp_seed`, `recovery_code`, `cookie`, `session` or `profile` field,
  and any value that looks like credential material rather than a reference.
  The refusal message names the binding as the remedy, not redaction in place.
- [x] 2.3 Tests for both directions, and a test that a reference alone is
  insufficient to obtain anything.

## 3. Documentation

- [x] 3.1 `docs/lifecycle-notebook-projection.md` §12: the custody story — where
  the credential lives, that each consuming system reaches it through its own
  binding, and that custody is not automation.
- [x] 3.2 `docs/notebook-projection-migration-runbook.md`: the custody step in
  sequence, and what an operator does when the interactive login is needed
  anyway.
- [x] 3.3 Record the session-class rule where a reader will hit it: the `nlm`
  profile is refreshable session state and is NOT a custody subject, on the
  same grounds `credential-contracts` already refuses distributing that class.

## 4. The bindings — one per consuming system

**FOUR OF THESE FIVE SURVIVE THE ARCHIVE UNTICKED, AND EACH IS A DECISION RATHER
THAN A LOOSE END** — restated at the archive act 2026-08-31 so a later reader
meets a disposition and not a blank box, on the shape
`2026-08-28-declare-sentinel-pin-vocabulary` § 5 established. **NOT ONE OF THE
FOUR IS BLOCKED ON ANYTHING THIS PACKET LEFT BROKEN**: 4.1 is a decision not to
ship a fixture, with the reason recorded in the box itself; 4.2 and 4.3 are
RESIDENCY statements — the live bindings belong to the consuming installs and to
openXdox's own lane, which is the ratified residency redirect and not work
withheld; **4.4 is an OPERATOR ACT**, the password's placement into
`kv-opensoft-xfactory-qa`, which nothing in this repository performs or witnesses
and which no author may tick. § 4.5 DID close, and it closed on the record — see
its own box.

- [ ] 4.1 DECLINED BY DEFAULT, with the reason recorded — a packaged fixture
  under `examples/credential-contracts/` showing two consuming systems would
  TRIP the validator: `shared-secret-identity` fires whenever two bindings in
  one template share a `secret_ref`
  (`scripts/validate-credential-contracts.py`), and two systems reaching ONE
  account's password is exactly that shape. Giving them distinct `secret_ref`s
  to satisfy the rule would misrepresent the estate (there is one secret), and
  relaxing the rule is a change to a check that exists to keep the dispatch and
  content credentials apart. So the requirement text carries the shape and no
  fixture is added. If a later change wants one, it must first decide whether
  `shared-secret-identity` should distinguish "two credentials collapsed into
  one" from "two consumers of one credential" — and updating the self-test
  count asserted in `tests/credential_contracts/` ("3 positive + 5 negative")
  rides with it.
- [ ] 4.2 NOT AN OPENXFACTORY SURFACE: the live xFactory sync-lane binding is
  declared in the install's `credentials/` tree, per the residency rule in
  `contracts/manifest.yaml` ("openxFactory ships no instance records"). Named
  here as the successor act; the shape is `provider`, `vault`, `secret_ref`,
  `owner`, `rotation_policy` with its own owner and its own access identity.
- [ ] 4.3 NOT THIS CHANGE: the openXdox binding is its own successor packet in
  its own lane, per Brett's ruling — openXdox pins openxFactory's contracts and
  declares its own binding, with its own access identity, grant, rotation
  visibility and audit trail.
- [ ] 4.4 OPERATOR ACT, not a task this change performs: the password (and any
  TOTP seed) is placed into `kv-opensoft-xfactory-qa` by Brett or an operator,
  under the landed custody rule, evidenced per `credential-contracts`. Nothing
  in this repository performs or witnesses that write.

- [x] 4.5 **DISCHARGED 2026-08-31, AND THE BOX IS TICKED ON THE SHIPPED SHAPE
  RATHER THAN ON THE SUCCESSOR'S EXISTENCE.** The owed successor is
  `add-binding-consumer-identity` — this box is the origin its `.openspec.yaml`
  cites — and it is not merely filed but REALIZED: the `consumer:` block naming
  the consuming system and the identity it fetches with is published in
  `contracts/schemas/xfactory-credential-contracts.schema.yaml`, landed by PR
  **#516** (squash `5e8a33cf`) and cut as **`contract-v2.4`** by PR **#526**
  (squash `afdf0e88`, tag published and peeling to that commit). **THAT SAME
  RELEASE IS WHAT FALSIFIED THIS BLOCK'S FIFTH SCENARIO**, struck by the § 6
  sweep in PR **#538** (squash `3a6a16e9`) under Brett Heap's consent, with the
  dated amendment note standing in its place inside the delta. The paragraph
  below is left standing as the state at filing, unedited: its "Today … carries
  no consumer or access-identity field" describes 2026-08-23 and is no longer
  true, which is what discharge looks like rather than a defect in the record.
  **What this tick does NOT claim**: the successor packet's own archive is a
  separate act, performed in the same pull request as this one and after it, in
  the safe order `release-realization` requires.
  NAMED SUCCESSOR, owed: extend the published binding shape so the
  per-system authority is REPRESENTABLE. Today
  `xfactory_credential_binding_template` requires only `[provider, secret_ref,
  owner, rotation_policy]` with optional `vault`, carries no consumer or
  access-identity field, and the validator compares no authorities — so two
  bindings using the same vault principal validate cleanly and the invariant is
  held by review rather than by the record. Adding that field is a
  `contracts/schemas/` change and therefore DOES carry the contract-release
  ritual (CHANGELOG allocation, manifest digest, `contract_bundle_version`
  bump, inventory rebuild, verify-commit, tag) — which is precisely why it is a
  successor and not smuggled into this change.

## 5. Validate green

- [x] 5.1 **DONE at the archive act, 2026-08-31.** Measured HERE and stable:
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` → 81 passed / 0 failed
  before, **80 passed / 0 failed** after (this change leaving the active set as
  its three requirements join the promoted set);
  `python3 scripts/validate-notebook-projection-hosting.py` → **`0 error(s)`**;
  `python3 scripts/validate-credential-contracts.py .` → **`0 error(s) -> PASS`**;
  `proposal-support verify` ok per-change and whole-corpus on BOTH sides of the
  move. `doc-health --family promotion-fidelity` → **No findings**, and
  `--family modified-block-currency` → **0 critical, 0 error, 0 warning, 9 info**,
  which is the pristine-`main` reading plus this packet's own info row and **no
  error of any kind**. The five pytest suites this box names are recorded green
  at the pull request tip, where the pair is whole.
  Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`, plus
  `pytest tests/notebooklm` and `pytest tests/credential_contracts` for the
  surfaces this change touches; `OPENSPEC_TELEMETRY=0 openspec validate --all
  --strict`; doc-health zero-new against a fresh same-clock `origin/main`
  baseline; `scripts/validate-notebook-projection-hosting.py` and
  `scripts/validate-credential-contracts.py .` both clean.
- [x] 5.2 **DONE, ASSERTED MECHANICALLY AT THE ARCHIVE ACT.** `git diff --stat
  origin/main -- contracts/` is **EMPTY** — not one contract byte moved — and
  `contracts/manifest.yaml:3` still reads `contract_bundle_version:
  contract-v2.5`. **No CHANGELOG entry, no manifest row, no inventory file, no
  tag.** `target_release: none` was correct at filing and is correct at the
  archive, which is the whole content of this box.
  Assert `contracts/` untouched and no bundle cut. `target_release:
  none` — the binding-template shape is already published.

## 6. Bookkeeping

- [x] 6.1 **DONE IN THIS ACT.** The README's OpenSpec Records block carries this
  change as an archived row pointing at
  `openspec/changes/archive/2026-08-31-add-notebook-hosting-credential-custody/proposal.md`,
  and the active row is gone rather than duplicated.
- [ ] 6.2 **SURVIVES THE ARCHIVE UNTICKED, AND IT IS NOT THIS ACT'S TO CLOSE —
  restated 2026-08-31.** `add-notebook-projection-identity` is STILL ACTIVE and
  still `Status: ratified`, so the generalization these requirements presume has
  not promoted. The obligation attaches to THAT change's archive, not to this
  one. It is the mirror of `add-binding-consumer-identity` § 7.3; whoever
  archives `add-notebook-projection-identity` discharges both.
  Reconcile with `add-notebook-projection-identity` at ITS archive: the
  generalization these requirements presume promotes then, and the two changes'
  `credential-contracts` text should be read together once both are promoted.

## 7. NOT part of this change

- Automated Google login. It is future work gated on proving the browser flow
  end to end, and custody does not advance it.
- Any change to the residency model that would let live binding instances live
  in openxFactory. If the ratifier wants the instances here, that rule changes
  first, in its own change.
- Rotating, replacing, or reading the account's credential.

## 8. The archive act — 2026-08-31

- [x] 8.1 **ARCHIVED ON BRETT HEAP'S ROUTE-1 RULING OF 2026-08-31** — the safe
      order `release-realization` requires — to
      `openspec/changes/archive/2026-08-31-add-notebook-hosting-credential-custody/`.

      **THIS ACT WAS PERFORMED TWICE, AND THE SECOND TIME IS THE ONE THAT LANDED.**
      A first attempt archived this packet at `bd2ccbc3` on the tree as it stood
      before the § 6 sweep. **PR #538** (squash `3a6a16e9`) then amended five
      ratified packets under one consent, THIS ONE INCLUDED, one minute before that
      attempt could merge — so the archive was rebuilt from `3a6a16e9` against the
      AMENDED packet rather than reconciled textually. What #538 changed here is
      § 6.6: **this block's fifth scenario, "The published binding shape cannot yet
      express the access identity", is STRUCK, not re-scoped**, falsified in every
      clause by `contract-v2.4`, with a dated amendment note standing in its place.
      That strike is why this block now carries FIVE scenarios where the first
      attempt archived six.

      **THE ARCHIVE GATE WAS ALREADY MET, AND IT WAS RE-READ RATHER THAN
      INHERITED.** The code surface landed **2026-08-26**: PR **#395**, merge
      `1dd822ea`, an ancestor of `main`. Every § 1–§ 3 box was verified AGAINST THE
      TREE: the `custody:` block naming the binding and never the secret, with
      `session_state_in_custody: false` and `self_hosted` left free of the
      obligation; `_check_custody` and the secret-shaped refusal running over the
      whole hosting block; `tests/notebooklm/test_validate_hosting.py`; and the
      three documentation surfaces including "The `nlm` session is NOT a custody
      subject". **No gap was found and nothing was built here.**

      **THE ACT.** `OPENSPEC_TELEMETRY=0 openspec archive
      add-notebook-hosting-credential-custody --yes` (openspec **1.2.0**) →
      `credential-contracts: update`, `lifecycle-notebook-projection: update`,
      `+ 2 added` and `+ 1 added`, `Totals: + 3, ~ 0, - 0, → 0`. It reported
      `Task status: 9/18` — **the CLI's reading at the moment it ran** — and this
      act then closed § 4.5, § 5.1, § 5.2 and § 6.1 and added this box, so **the
      archived file's end state is 14/19**. The five that stay open are § 4.1–§ 4.4
      and § 6.2, each with its own restated disposition. Neither count corrects the
      other.

      **THE MECHANISM WAS `openspec archive`, NOT `proposal-support archive`**, and
      the choice is deliberate: that wrapper refuses any `^- \[ \]` line and cannot
      tell an operator act from unfinished work, and § 4.4 is an operator act no
      author may tick. Its two additions were run anyway on both sides of the move —
      `proposal-support verify` ok per-change and whole-corpus, and packaging, a
      lawful no-op for an origin with no `supporting-docs/` folder. Precedent:
      `2026-08-28-declare-sentinel-pin-vocabulary` and the three sibling archives of
      2026-08-27.

      **PROMOTION VERIFIED BYTE-FOR-BYTE, and there was no scenario-completeness
      exposure to begin with**: both deltas are **pure ADDED**, with no MODIFIED,
      REMOVED or RENAMED block anywhere, so no canon scenario set was being
      restated. Measured anyway: **3 requirements in, 3 out, all three bodies
      BYTE-IDENTICAL (3/3), 13 scenarios in, 13 out**; `credential-contracts`
      **7 → 9 requirements and 24 → 33 scenarios**; `lifecycle-notebook-projection`
      gains one requirement. Neither ADDED title existed in canon beforehand,
      checked by `grep`. `doc-health --family promotion-fidelity` → **No findings**.
      The thirteen-scenario figure is the post-#538 count; the pre-sweep packet
      carried fourteen.

      **THE KNOWN CLI HAZARD DID NOT FIRE.** `.openspec.yaml` moved with the packet:
      blob `36d76fdc56b58b46333d9d20ad210e0584c9119c`, identical either side.

      **WHAT THIS ACT UNBLOCKED.** `add-binding-consumer-identity` carries a
      `## MODIFIED Requirements` block over a requirement THIS packet ADDS. Its
      § 7.2 pre-archive assertion read **0** before this act and **1** after it, and
      `openspec archive` had ABORTED on that packet with *"MODIFIED failed for
      header … - not found"*. That archive is the next commit. #538 says the same in
      its own words: *"custody archives first, and `add-binding-consumer-identity`
      stays held while the title is unpromoted."*
