Status: record
Reviewer role: QA Lead (alignment review against openxFactory ratified requirements, read-only) — 2026-08-26
Subject proposal: openspec/changes/split-openxwallet-repo/proposal.md
Dispositions ruled by: the change lead, 2026-08-26 — all MISMATCH findings APPLIED;
all GAP findings APPLIED as additions inside the declared scope; the missing-`specs/`
finding DEFERRED to the specs phase, with the eleven requirement titles recorded here
for the specs author.

# QA Lead review — `split-openxwallet-repo`

**Reviewed against:** promoted specs in `openspec/specs/`, the ratified-but-active
`add-trust-anchor` and `add-wallet-carried-review-authority` deltas,
`contracts/openxwallet*/`, `contracts/manifest.yaml`, `docs/contract-versioning-policy.md`,
and the live consumer trees (LedgerxFactory, OpsxFactory).

**Headline:** the proposal is testable in most places and unfalsifiable in six, and the
two MODIFIED deltas do not say what they modify — the trust-anchor delta describes a
code change where the requirement's defect is a dangling cross-corpus reference, and the
review-authority-intake delta misquotes the requirement it amends and misses that its
scenario becomes unsatisfiable. The consumer surfaces are undercounted on both sides.

---

## 1. No spec deltas — and the eleven titles the specs author needs

**Finding (verbatim).** MISMATCH — no spec deltas (DEFERRED). The eleven titles,
verified byte-identical in promoted specs and the archived delta: `A wallet is a key,
never a record of a key` · `Authority travels as attenuated grants, never as keys` ·
`Use requires proof of possession, not presentation` · `Custody is declared and bounds
what a signature evidences` · `Every exercise is key-attributed` · `Revocation
propagates through the chain` · `Distinct-holder constraints are expressible` · `The
capability is an authority control, never an identity substrate` — and `An agent holder
declares its composition` · `A composition change revokes the agent's grants
immediately` · `Agent authority is grant scope, not a parallel vocabulary`. Note
`promotion_fidelity.py` keys on (capability, normalized title) — one character of drift
leaves the 2026-08-08 ADDED writer authoritative. Write these titles INTO the proposal's
Removed Capabilities § verbatim (they were only described, not listed).

**Disposition: the missing `specs/` deltas are DEFERRED to the specs phase; the title
list is APPLIED to the proposal.** All eleven re-verified this session against
`openspec/specs/openxwallet/spec.md` (`:6`, `:28`, `:49`, `:71`, `:93`, `:113`, `:133`,
`:155`) and `openspec/specs/openxwallet-agent-profile/spec.md` (`:6`, `:27`, `:50`), and
they are now listed verbatim as a numbered 1–11 block in the proposal's Removed
Capabilities §, with the `promotion_fidelity.py` join-key warning stated beside them.

**For the specs author — the exact eleven titles, in delta order.**
`## REMOVED Requirements` for capability `openxwallet`:

1. `A wallet is a key, never a record of a key`
2. `Authority travels as attenuated grants, never as keys`
3. `Use requires proof of possession, not presentation`
4. `Custody is declared and bounds what a signature evidences`
5. `Every exercise is key-attributed`
6. `Revocation propagates through the chain`
7. `Distinct-holder constraints are expressible`
8. `The capability is an authority control, never an identity substrate`

`## REMOVED Requirements` for capability `openxwallet-agent-profile`:

9. `An agent holder declares its composition`
10. `A composition change revokes the agent's grants immediately`
11. `Agent authority is grant scope, not a parallel vocabulary`

One character of drift in any of these eleven strings silently defeats the removal.

## 2. `shared-contract-ownership` — and two things `neutral-product-pin` must state

**Finding (verbatim).** GAP — shared-contract-ownership `:139-170` (covered by Architect
#1). Additionally state in `neutral-product-pin`: openXwallet carries the vendored
envelope schema at `contracts/schemas/hermes-job-envelope.schema.yaml` (so the `:142`
publisher marker test is satisfied in the new repo), and `contracts/<product>-pin.yaml`
is a reverse-direction pin outside `:146`'s stack.yaml rule.

**Disposition: APPLIED (GAP added to scope),** union with Architect #1. Both statements
now sit in the `neutral-product-pin` bullet, with `:142` and `:146` cited by line.

## 3. The trust-anchor MODIFIED delta describes the wrong thing

**Finding (verbatim).** MISMATCH — trust-anchor MODIFIED delta (~270-281) describes a
code change; the requirement "Declared chain custody bounds what a certificate
evidences" (`openspec/changes/add-trust-anchor/specs/trust-anchor/spec.md:69-99`) only
says "composing with `openxwallet`'s ratified rule that custody caps what a signature
evidences instead of restating a second custody model" — no resolution path. FIX: the
modification is the dangling cross-corpus reference: "…composing with the `openxwallet`
capability's ratified rule, consumed from `opensoft/openXwallet` at the pin recorded in
`contracts/openxwallet-pin.yaml`, that custody caps what a signature evidences…" plus a
new scenario: "WHEN the pinned openXwallet checkout is uninitialized or its
custody-registry digest disagrees with the pin THEN the custody question is refused
rather than resolved."

**Disposition: APPLIED,** verbatim. The requirement text and range were re-verified at
`add-trust-anchor/specs/trust-anchor/spec.md:69-99`. The delta bullet now leads with
"the modification is a dangling cross-corpus reference, not a code change", carries the
rewritten clause and the new scenario, and demotes the validator changes to "P3's
surface, not the requirement's text".

## 4. The review-authority-intake delta misquotes its own target

**Finding (verbatim).** MISMATCH — review-authority-intake delta (~284-285) misquotes:
the requirement is titled "A grant with no reader in a required check confers nothing"
(`add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:30-40`; "A
review-authority grant SHALL confer no authority until a named validator that reads it
runs as a REQUIRED check on the repository that holds the register"). Scenario `:38-39`
"WHEN `scripts/validate-openxwallet.py` (or the register's own validator) is present in
the repository but appears in no workflow that is a required check" becomes
unsatisfiable after P3. FIX: quote the title verbatim; state the scenario rewrite "…is
reachable in the repository, in-tree or through a digest-pinned submodule, but appears
in no workflow that is a required check".

**Disposition: APPLIED,** verbatim. Title, requirement sentence, scenario range and
scenario text all re-verified at `:30-40`. The proposal's paraphrase "*an intake entry
with no reader confers nothing*" is gone.

## 5. README ranges

**Finding (verbatim).** MISMATCH — README ranges (union with Architect 7-9,15):
`:217-228`, `:286-293`, `:310`, `:805`, `:873-927` (naming `:896`, `:909-912`,
`:920-921`), `:2523-2536`, `:2612`.

**Disposition: APPLIED as the union.** All seven citations now appear in the
openxFactory Impact bullet. `:217-228` was taken over the architect's `:217-229` as
ruled (line 229 is blank). Two accuracy notes carried in
`alignment-stack-architect.md` §§ 8–9: `:310` is inside the **Trust anchors**
contract-index entry, and the stale "advisory until an operator marks it required"
phrase is at `:896-897` rather than `:909-912`.

## 6. The LedgerxFactory repoint surface is undercounted

**Finding (verbatim).** MISMATCH — LedgerxFactory repoint surface undercounted. FIX
replace the LedgerxFactory bullet's file list with: `tests/validate_wallet_estate.py:47-66`
(5a/5b), `specs/016-posting-segregation-of-duties/quickstart.md:15`, `plan.md:27`,
`spec.md:63`, `data-model.md:5` (a COMMIT pin `e5554028` to openxFactory paths — needs a
new repo + commit, not a path edit; name as a distinct item),
`openspec/changes/modify-ledgerx-posting-authority-for-segregation-of-duties/tasks.md:81`
(an ACTIVE change), `README.md:220` (not `:112-135`, which is concept prose), plus the
`tests/validate_document_estate_surface.py:1046-1075` ownership comment.

**Disposition: APPLIED,** verbatim, with every citation re-verified in the LedgerxFactory
tree. The two distinct kinds of work are called out as such: the `e5554028` commit pin
(which also recurs at `plan.md:26`, `quickstart.md:4`, `spec.md:376`) and the edit
inside the ACTIVE `modify-ledgerx-posting-authority-for-segregation-of-duties` change.

## 7. Open-task count

**Finding (verbatim).** MISMATCH — "14 of its 21 open tasks" → "15 of its 21 open tasks"
(§6 S3 = 8, §7 S5 = 7) at ~110.

**Disposition: APPLIED,** with the arithmetic shown inline ("§6 S3's eight plus §7 S5's
seven") so the count is checkable rather than asserted.

## 8. `identity-brokering` is not declared and should say so

**Finding (verbatim).** GAP — add to "Declared NOT modified": "`identity-brokering` —
NOT declared. Its two `openxwallet` references
(`openspec/changes/add-identity-brokering/specs/identity-brokering/spec.md:196`, `:211`)
name the capability, not a path or a corpus member; after the split they resolve to
`opensoft/openXwallet` through `contracts/openxwallet-pin.yaml`."

**Disposition: APPLIED (GAP added to scope),** verbatim. Both lines re-verified: `:196`
"grants and `openxwallet` holders rather than from anything the broker" and `:211` "THEN
it receives a grant under `credential-contracts` / `openxwallet`" — neither is a path.

## 9. No `## Realization evidence` section

**Finding (verbatim).** GAP — add a "## Realization evidence" section (per
`openspec/specs/release-realization/spec.md:22-46`): one row per surface — repository, PR
number, merge commit, the check name + run id that went green; for the two ruleset
states, the `GET repos/<owner>/<repo>/rules/branches/main` output showing
`required_status_checks → [<token>]`; openXwallet's first green `wallet-validation` and
`pytest-suite` runs plus the byte-identity proof are the runnable-surface half. Surfaces:
opensoft/openXwallet (P2), openxFactory (P2.5 deprecation minor; P3 major), xFactory
(P4), LedgerxFactory (P5a, P5b), OpsxFactory (P5b), the two rulesets.

**Disposition: APPLIED (GAP added to scope).** A new `## Realization evidence` section
sits between `## Impact` and `## Open questions`, carrying an eight-row surface table
(the P2.5 row included, per Architect #11) and a separate two-row ruleset-state table,
each with the `GET .../rules/branches/main` evidence form named. Stated in the section
as "a gate, not a report".

## 10. The reverse vendoring is not licensed by `:25-27`

**Finding (verbatim).** GAP — `shared-contract-ownership:25-27` "Subsystem adapter needs
a contract" is scoped to INSTALL repos, so the reverse vendoring (~347-350 "needs no
delta on either reading") is not licensed by it. FIX: say so, and add to
`neutral-product-pin`: "a neutral product repository MAY keep a digest-pinned copy of
one openxFactory contract, and MUST identify the openxFactory contract version it pins"
(mirroring `:27`).

**Disposition: APPLIED (GAP added to scope).** Verified: the scenario's WHEN reads "an
install repo needs a runtime adapter, generated client, smoke fixture, or pinned schema
copy". The permission is now a limb of `neutral-product-pin`, and the ## Declared NOT
modified bullet states plainly that `:25-27` does not license it.

## 11. Stale corpus counts carried through the move

**Finding (verbatim).** GAP — add to Impact: "Carried stale, deliberately NOT corrected:
`contracts/manifest.yaml:1968-1969` says 16/33 and `contracts/README.md:108` says
nineteen rules and 16/33; the tree is 17 positives, 36 negatives, 21 rules `(a)`-`(u)`.
Correcting them inside a byte-identical move would destroy the property the move is safe
on; the correction is a successor in openXwallet."

**Disposition: APPLIED (GAP added to scope).** All six numbers independently re-counted
this session: 17 positives, 36 negatives under `examples/negative/`, and 21 rule letters
`(a)`–`(u)` in `scripts/validate-openxwallet.py`. Added to Impact AND as a named
successor, so the deliberate staleness has an owner.

## 12. Six unfalsifiable bullets

**Finding (verbatim).** GAP — make six bullets falsifiable: (a) P2 "prove byte-identity"
→ "for each of the eight rows at `contracts/manifest.yaml:1967-2082`, `sha256sum` at
openXwallet `wallet-v1.0` equals the recorded `sha256:`, and a diff of the carved subtree
against openxFactory's `contracts/openxwallet*/`, `scripts/validate-openxwallet.py`,
`scripts/wallet-yaml-syntax-gate.py`, `tests/wallet_yaml_syntax_gate/` is empty (spec
prose excepted per the named carve-out)". (b) R6 "Zero refactor" → "`git diff` on
`scripts/validate-openxwallet.py` between openxFactory HEAD and openXwallet `wallet-v1.0`
touches only `ENVELOPE_SCHEMA_PATH` (`:218`)". (c) P3 "the registry path changes" →
"`scripts/validate-trust-anchor.py` resolves `OPENXWALLET_REGISTRY_PATH` from
`contracts/openxwallet-pin.yaml` and exits 2 with a named refusal on an uninitialized
submodule or a digest disagreement; `tests/trust-anchor/` covers both". (d) RATIFIES #5 →
quote the replacement text of xFactory CLAUDE.md working rule #1 verbatim (read
`/home/brett/projects/xFactory/CLAUDE.md` rule 1 first and give the exact before/after).
(e) Amendment 2 → per Amendment 1's shape (`docs/openxdox-naming.md:84-100`), give the
new section text AND the inline pointer at `:23-25`, whose sentence names two exceptions
and must stay grammatical when one leaves ("the lowercase `openxFactory` spelling is the
family exception, not the rule"). (f) rule (d) "created LAZILY" → "a
`<Domainx><Product>` repository SHALL NOT be created before the domain tree carries at
least one artifact of the product's profile kind".

**Disposition: APPLIED (GAP added to scope) — all six.** (a) in the P2 bullet, with the
carve-out cross-referenced. (b) in R6, `ENVELOPE_SCHEMA_PATH` confirmed at
`scripts/validate-openxwallet.py:218`. (c) in the P3 bullet. (d) the before-text was read
from `/home/brett/projects/xFactory/CLAUDE.md` § "Working rules" item 1 and is quoted
verbatim, with the replacement quoted beside it as a block quote. (e) Amendment 2 now
carries a full draft section in Amendment 1's shape plus an explicit before/after for the
`:23-25` pointer. (f) rule (d) restated as a SHALL NOT.

## 13. The OpsxFactory path is missing its prefix, and there are more references

**Finding (verbatim).** MISMATCH — OpsxFactory path (~395-397) must carry the
`openspec/changes/add-keycloak-administration-workflow/` prefix; enumerate all five
references (`supporting-docs/identity-pki-administration.md:59`, `:294`, `:417` [the only
path-bearing one], `credentials/requirements.yaml:514`,
`workflows/keycloak-administration.yaml:56`; `specs/keycloak-administration/spec.md:150`
is pathless) with "needs nothing" covering all five.

**Disposition: APPLIED.** All six references enumerated with the prefix supplied, and the
two root-level files (`credentials/requirements.yaml:514`,
`workflows/keycloak-administration.yaml:56`) flagged as being OUTSIDE that prefix, which
the finding's own list implies. `:417` is stated as the only path-bearing reference and
the only P5b repoint; the other five "need nothing".

## 14. The ordered-delta rule is applied by parity, not by its letter

**Finding (verbatim).** GAP — `release-realization:64-79` ordered-delta rule's letter
covers a requirement already MODIFIED; add-trust-anchor and add-wallet-carried-review-authority
ADD theirs. FIX at ~272-275: "the rule's letter covers a requirement already MODIFIED;
these are ADDED, so this proposal applies it by parity and declares the parity rather
than implying the letter."

**Disposition: APPLIED (GAP added to scope).** Verified: the requirement reads "a
proposal modifying a requirement already modified by an active ratified change", and its
scenario repeats "already modifies". The parity declaration is stated once in the
`trust-anchor` bullet and referred back to from the `review-authority-intake` bullet
("by the same parity reading").

## 15. Validator hard-exit range

**Finding (verbatim).** MISMATCH — `validate-trust-anchor.py:2582-2591` → `:2582-2586`
(covered).

**Disposition: APPLIED.** Verified: the `if not OPENXWALLET_REGISTRY_PATH.is_file()`
block runs `:2582-2586` and `:2587` is blank. Corrected in all four places it appeared.

---

## Disposition summary

| # | Dimension | Severity | Disposition |
|---|---|---|---|
| 1 | no spec deltas; the eleven titles unlisted | MISMATCH | **deltas DEFERRED to specs phase**; titles APPLIED |
| 2 | `neutral-product-pin` must state the vendored copy + reverse pin | GAP | APPLIED (GAP added to scope) |
| 3 | trust-anchor delta describes code, not the dangling reference | MISMATCH | APPLIED |
| 4 | review-authority-intake delta misquotes its target | MISMATCH | APPLIED |
| 5 | README ranges | MISMATCH | APPLIED (union with Architect 7–9, 15) |
| 6 | LedgerxFactory surface undercounted | MISMATCH | APPLIED |
| 7 | 14 → 15 of 21 open tasks | MISMATCH | APPLIED |
| 8 | `identity-brokering` not declared, unstated | GAP | APPLIED (GAP added to scope) |
| 9 | no `## Realization evidence` section | GAP | APPLIED (GAP added to scope) |
| 10 | `:25-27` does not license the reverse vendoring | GAP | APPLIED (GAP added to scope) |
| 11 | stale corpus counts carried through the move | GAP | APPLIED (GAP added to scope) |
| 12 | six unfalsifiable bullets | GAP | APPLIED (GAP added to scope) — all six |
| 13 | OpsxFactory prefix + reference count | MISMATCH | APPLIED |
| 14 | ordered-delta rule applies by parity, not letter | GAP | APPLIED (GAP added to scope) |
| 15 | validator hard-exit range | MISMATCH | APPLIED |

**Remaining gate failure:** the change still has no `specs/` deltas, so
`OPENSPEC_TELEMETRY=0 openspec validate split-openxwallet-repo --strict` reports exactly
one error — "Change must have at least one delta" — by ruling, as the specs phase's
work. Nothing else in this reviewer's set is outstanding.
