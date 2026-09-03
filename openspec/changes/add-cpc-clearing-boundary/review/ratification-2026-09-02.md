# Proposal Ratification: add-cpc-clearing-boundary

Status: ratified
Decision date: 2026-09-02
Ratifier: Brett Heap (repository owner) — in-session, on the recorded word
Ratified: 2026-09-02 by Brett Heap (repository owner) — in-session, verbatim:
*"Ratify + merge openxFactory #560"*.
Ratified baseline: head `33fa2b54` — "Re-validate add-cpc-clearing-boundary
against #555 on main; standing wording is now fact" — `proposal.md`,
`design.md`, `tasks.md`, `.openspec.yaml`,
`specs/clearing-dispatch-boundary/spec.md` (THREE MODIFIED requirements),
and `specs/factory-origin-identity/spec.md` (SIX ADDED requirements, a new
capability) as they stood at that commit.

## Decision

**RATIFY, AND MERGE.** Brett's word carried both acts in one instruction,
unlike `add-clearing-dispatch-boundary`'s ratification (`review/
ratification-2026-09-01.md`), where ratify and merge were separate acts
because that packet's own merge was gated on an inherited pytest failure.
No such gate applies here: this packet carries no code surface beyond the
governance register family, its own `openspec validate --strict`, `--all
--strict`, `proposal-support.py verify`, and doc-health families are green at
the ratified head (recorded under Verification below), and the ordering
precondition — `add-clearing-dispatch-boundary` (#555) merging before this
packet — already discharged on 2026-09-02. Ratification is recorded here;
the merge itself is `opensoft/openxFactory#560`, executed as the second half
of the same operator word, not a separate decision.

## What is ratified

**Three MODIFIED requirements on `clearing-dispatch-boundary`**, each carried
verbatim from the basis (`add-clearing-dispatch-boundary`, ratified
2026-09-01, PR #555) with additions marked in place, every original scenario
retained (177 basis units, none lost), and each carrying its own `Modified
over` marker inside its own requirement body per
`govern-sibling-added-modified-deltas`:

1. *Work crosses the boundary only as a sealed bounded request* — field (10)
   becomes a required signature, covering all ten declared fields, for a
   registered originator; no eleventh field, no second digest vocabulary.
2. *Every verifiable field is verified against the provider's authoritative
   API* — origin-signature verification added as a third, conjunctive
   verification class; policy-checked fields resolved from the
   permitted-operations register rather than read from the bundle.
3. *Every dispatch is recorded, and the single door is attested rather than
   assumed* — the periodic attestation's read set widens by one field:
   workspace-disposal evidence, absent or empty, is an UNATTESTED DISPOSAL.

**Three ADDED requirements on the same capability**, which the basis has no
counterpart to: result attestation on the originating repository's hosted
infrastructure after the return verifies (sign-on-return); workspace disposal
evidence as a recorded field of the dispatch record; and returned output
re-served to the originator from the clearing side's own sealed object (the
inbound half of the re-seal, which the basis states only outbound).

**Six ADDED requirements under the new capability `factory-origin-identity`**:
one registered Ed25519 origin identity per originating repository in a
sibling register; public key references only; hosted-environment custody of
the private half; a checked disjointness rule across the two register
families; the register's own staleness bound and ceiling; and a permanently
human-only register surface.

**The register-home ruling.** Origin keys live in a SIBLING register at
`governance/factory-identity/`, not an extension of the review-authority
intake register — design D1, decided in this packet and SINCE CONFIRMED BY
THE OPERATOR (design.md D1 header). The reason is structural, not stylistic:
the ruling's act-distinctness requirement becomes enforceable across two
registers read by two readers, where inside one file it would be a field
predicate one mistyped `act:` away from collapse.

**The origin-key and sign-on-return rulings.** Both requirement classes trace
to Brett Heap's 2026-09-01 same-day extension comment on `opensoft/
codexFactory#156`, which this packet's `Origin:` header cites and which
`add-clearing-dispatch-boundary` does not reach:

> 2. **Seat-return signing = OPTION (b), sign-on-return.** The CPC produces
> UNSIGNED seat results inside the sealed return object; a HOSTED codexFactory
> workflow … verifies the returned bundle's provenance and digest, then signs
> the seat results … Seat private halves never touch the CPC.
>
> 3. **Per-factory ORIGIN keys.** Each domain factory holds one Ed25519 origin
> key (private half in its hosted environment; public half registered in
> openxFactory, register/wallet/grant pattern) and signs its bounded request
> manifests; xFactory's clearing workflow verifies origin signatures against
> the registered public key, alongside — never instead of — GitHub API
> provenance checks.

## Review history

**Three adversarial rounds ran on 2026-09-01**, each producing a verdict this
record carries rather than re-litigates:

1. **NOT READY** (commit `c175f02f`, "Re-scope to the extension delta over the
   ratified add-clearing-dispatch-boundary"). **Finding A-1**: the first draft
   did not know `add-clearing-dispatch-boundary` already existed — RATIFIED
   2026-09-01, ten requirements from the same operator ruling, realization
   live on xFactory main — and had re-authored roughly seven of those
   requirements in divergent vocabulary without citing the basis. That draft
   was withdrawn. The packet was re-scoped to a `## MODIFIED Requirements`
   block over `clearing-dispatch-boundary` (two requirements at that point)
   plus what the basis has no counterpart to, `.openspec.yaml` was corrected
   to run its duplicate check against active changes and recent
   ratifications rather than the promoted index alone (the check that would
   have caught the collision earlier), and findings A-2 through A-10 fixed
   the manifest-field count, the register-resolved policy fields, the
   disjointness rule, and the impact-map corrections.
2. **RATIFY WITH EDITS** (commit `4fc791c1`, "Second-review edits: merge
   order, the digest carve-out, tier alignment, inbound re-seal"). Four
   findings: the merge-order trap now stated in proposal.md, design.md and
   the README (#555 must merge first or its contested
   `modified-block-currency` warnings enter the nightly baseline uncited);
   the digest-construction carve-out (design D12) naming two constructions —
   canonical JSON for the manifest, pending a tranche-3 `digest_subject`
   widening, and plain byte hashes for per-file content — so neither reads as
   a forbidden second vocabulary; a dropped `authority tier` register-row
   field the spec's row enumeration never named; and the inbound re-seal
   added as its own requirement rather than left to the symmetry codexFactory
   PR #165 assumed. The capability grew to 2 MODIFIED + 3 ADDED.
3. **RATIFY WITH EDITS** (commit `8dc27d2e`, "Per-requirement Modified over
   markers; declare the attestation extension"). **Blocking finding**: the
   `Modified over` marker sat at section level, under `## MODIFIED
   Requirements`, but `govern-sibling-added-modified-deltas` requires the
   marker PER REQUIREMENT — a section-level paragraph leaves every
   requirement in the block declaring nothing, and the pairing arm reports
   each as unmarked. Each MODIFIED requirement was given its own marker
   inside its own body, proven both ways: with #555's change dir staged into
   the tree, `modified-block-currency` reported 0 critical / 0 error / 0
   warning; with it removed, exactly three warnings (one per MODIFIED
   requirement), the absent-basis condition rather than a marker defect. The
   same round declared the attestation extension explicitly — the ADDED
   workspace-disposal requirement had made disposal evidence a field of the
   dispatch record and then had the periodic attestation read it, an
   extension of a ratified requirement written from outside it. That coupling
   became the third MODIFIED block (design D14) rather than an implicit
   reach-in. The capability reached its ratified shape: 3 MODIFIED + 3 ADDED,
   177 basis units, 0 lost.

**Confirmed** (commit `33fa2b54`, 2026-09-02, "Re-validate
add-cpc-clearing-boundary against #555 on main; standing wording is now
fact"). This is a re-validation, not a fourth adversarial round: the catch-up
merge of `origin/main` brought the now-merged `add-clearing-dispatch-boundary`
into this branch's tree, and re-validation confirmed the three
previously-contested `modified-block-currency` warnings on this packet's
MODIFIED blocks are gone. `tasks.md` §1.9/§1.10 and the proposal's Standing
section were updated from "#555 merges first" (a condition) to "#555 merged
2026-09-02" (a fact) — the merge order was honored, not merely intended.

## Ordering facts

- `add-clearing-dispatch-boundary` (`opensoft/openxFactory#555`) **MERGED
  FIRST**, 2026-09-02T09:16:29Z, squash commit `ab0bb2dd2e642fce43bee3d02128bafd664d3be3`
  — before this packet's ratification and before its own merge.
- **`opensoft/xFactory#201`** ("Dispose the three add-cpc-clearing-boundary
  pairing warnings, citing add-clearing-dispatch-boundary") — the belt behind
  the merge-order control, three disposition rows for
  `health/dispositions.yaml` at the aggregation root — was **CLOSED AS
  UNNECESSARY**: the intended order (#555 first) held, so the rows the PR
  would have added were never needed. `tasks.md` §1.10/§5.3 record this rather
  than pretending the rows landed.
- The caught-up head `33fa2b54` (this packet's branch, `origin/main` merged
  in) validates clean: `openspec validate --all --strict` reports **85
  passed, 0 failed**, and `modified-block-currency` reports **0 warnings** for
  this change's three MODIFIED blocks (down from three contested warnings
  while the basis was unmerged) — see Verification below for the run against
  this exact ratified head.

## What ratification authorizes

**Realizations named in the impact map, none performed by this act:**

1. **This repository, post-ratification** (`tasks.md` §2, one governed act):
   the `governance/factory-identity/` register rows
   (`register.yaml`/`wallets/`/`grants/`/`attestations/`), the disjointness
   validator (§2.5), and the codexFactory floor-file exact-set entry (§2.7) —
   named as landing together because the floor file is compared as an exact
   set and a register with no consuming floor entry would fail that
   comparison the moment it existed. Also blocking within this section:
   §2.9's tranche-3 `digest_subject` widening, without which the origin
   signature over the manifest is reported UNREALIZABLE rather than
   satisfied.
2. **xFactory** (`tasks.md` §3) — origin-signature verification and
   register-resolved operation constraints in the live clearing workflow;
   workspace-disposal evidence as a dispatch-record field; register-view
   staleness enforcement.
3. **codexFactory** (`tasks.md` §4) — the hosted packaging workflow signing
   manifests with the origin key; the hosted sign-on-return workflow
   verifying before signing; the floor-file update of §2.7 landed in the same
   governed act; and draft PR #165 (`adopt-bundle-shaped-deliberation`),
   which needs the governed register change adding a `deliberation`
   operation that does not exist yet.
4. **openXwallet** (`tasks.md` §5) — scoping the review-authority reader's
   wallet and grant resolution to its own register, the only realization that
   can make the disjointness rule's read-time refusal true in both
   directions.

**What this ratification does not do:**

- **It does not move a contract byte.** No `contracts/` artifact is added or
  changed by this change (`target_release: none`); OQ2 resolves to REFERENCE
  and no manifest schema is cut.
- **It does not perform any of the four realizations above.** Each is
  authorized to proceed on its own verification bar, in its own repository,
  and none is executed by this record.
- **It does not settle OQ1, OQ3, or the tranche-3 widening** — carried below,
  not ruled.
- **It does not retroactively re-open the merge-order question.** The
  ordering obligation (`release-realization`'s ordered-deltas rule; this
  packet's MODIFIED block written over #555's addition) already discharged
  when #555 merged first; this record states that fact, it does not decide
  it.

## Open questions — carried, not re-litigated

- **OQ1** (how a projection of the `factory-identity` register reaches the
  clearing workflow) — **OPEN**. Four shapes sketched in `design.md`
  (scheduled projection refresher, checked-in digest-pinned projection,
  live cross-repository read, runtime authority lookup), none chosen. D9's
  honesty clause stands until it resolves: whatever staleness bound the
  chosen shape supports is the real ceiling on revocation.
- **OQ3** (who scopes the review-authority reader so the disjointness rule's
  read-time refusal becomes true) — **OPEN**, named as an openXwallet
  dependency task (`tasks.md` §5.1/§5.2). The reader is pinned vocabulary
  owned outside this repository; three routes are named in `design.md`, none
  chosen.
- **The tranche-3 `digest_subject` widening** (`tasks.md` §2.9, design D12) —
  not an OQ but an unrealizability condition carried the same way: the
  canonical `xfc-jcs-sha256-1` construction's closed `digest_subject`
  enumeration has no manifest subject today, so the origin-signature
  requirement over the manifest is reported UNREALIZABLE, not satisfied,
  until a tranche-3 widening of SUBJECTS lands — never a second construction,
  the one way that enumeration's own header says it is meant to move.

None of the three is a blocking condition on this ratification; each is
already declared as open or unrealizable in the ratified text itself, per
`tasks.md`'s own "ruling or carrying" framing.

## Verification (at ratified head `33fa2b54`, re-confirmed for this record)

- `openspec validate add-cpc-clearing-boundary --strict`: valid, zero issues.
- `openspec validate --all --strict`: 85 passed, 0 failed.
- `python3 scripts/proposal-support.py . verify`: ok.
- doc-health families `proposal-origin`, `status-validity`,
  `location-conformance`, `modified-block-currency`, `promotion-fidelity`:
  exit 0, no error or critical finding; `modified-block-currency` reports 0
  warnings for this change's three MODIFIED blocks.

## Next

Realization per `tasks.md` §2 (this repository — register family,
disjointness validator, and codexFactory floor entry as one governed act,
blocked in part on §2.9's tranche-3 widening), §3 (xFactory), §4 (codexFactory,
including draft PR #165), and §5 (openXwallet reader scoping). Merge of this
packet's own pull request, `opensoft/openxFactory#560`, proceeds immediately
under the same operator word this record ratifies on. Archive per `tasks.md`
§6.2 only after `add-clearing-dispatch-boundary` archives and this packet's
own realization evidence is green — the ordering obligation this packet
carries in its front matter.
