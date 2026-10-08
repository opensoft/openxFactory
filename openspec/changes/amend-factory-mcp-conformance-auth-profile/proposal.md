---
code_surface: openxFactory — `contracts/factory-mcp/declaration.schema.json` and its synthetic example under `contracts/factory-mcp/examples/` (the authorization block, the `auth` support concern), `scripts/validate-factory-mcp.py` (the authorization checks and their stable codes), `tests/factory-mcp/` (red-first tests for every refusal this change names, including the narrowed *Unavailable dependency* scenario), `docs/factory-mcp-conformance.md` (the runbook), and, at the contract cut, `contracts/manifest.yaml`, `contracts/CHANGELOG.md` and `contracts/releases/<version>.digests.yaml`. THIS PACKET AUTHORS NO CODE BYTE: landing it is corpus text only (its five files, one README *Active changes* bullet, the machine-seeded rows in `tests/sequenced_after/corpus-ledger.yaml`, and the one `_LEDGER_SUBJECTS` data row the `modified-block-currency` self-gate requires for its `## MODIFIED` block). The realization follows through one Speckit feature after ratification.
target_release: deferred-allocation — the factory MCP declaration is unbundled and unreleased today (`contracts/factory-mcp/` has no row in `contracts/manifest.yaml`, whose bundle is `contract-v4.0`). Its realization registers the declaration in the contract bundle for the first time, at the next additive minor after `contract-v4.0` (`contract-v4.1` if no other cut lands first). `docs/contract-versioning-policy.md` § Bundle Realization Order allocates that number AT THE CUT and forbids reserving it now, so it is named here and not declared. The cut is realization work, under its own claim of row 4 (contract cuts) on #630.
sequenced_after: [add-factory-mcp-conformance]
---

# Proposal: amend-factory-mcp-conformance-auth-profile

Status: ratified
Ratified: 2026-10-08T20:2xZ by Brett Heap (openxFactory repository owner) - in session to lane `openXfactory-5`, verbatim *"Ratify, OQs as recommended (Recommended)"*; RULED on the estate's lane register at 2026-10-08T20:33:25Z. RATIFIED AS DRAFTED, with all six open questions of `design.md` (OQ-1 to OQ-6) adopted at the recommended answer, so no requirement or scenario text moved. The word is a ratify word only: it is not a landing word and it archives nothing; record at review/ratification-2026-10-08.md
Kind: proposal
Proposed: 2026-10-08, in lane `openxfactory-5` (display `openXfactory-5`), on
Brett Heap's three rulings of that day, recorded verbatim below.
Origin: the three items the archive of `add-factory-mcp-conformance`
([#1252](https://github.com/opensoft/openxFactory/pull/1252)) recorded as
still awaiting his rulings. `origin: ad_hoc`; see `.openspec.yaml`.
Claims: this change path is CLAIMED on the lane register
(`opensoft/brett-wip` commit `55a63c0d`); the README Records block is claimed
on [#630](https://github.com/opensoft/openxFactory/issues/630)
(comment `6066626855`). That claim names one new corpus-ledger row as its
expected movement; the seeder also flipped the partner row
`add-factory-mcp-conformance` from `sole` to `co-modifier`, and the claim's
amendment to say so is owed before landing (`tasks.md` 1.3).

**RATIFIED AS DRAFTED, 2026-10-08.** This packet was filed `Status: draft`.
The three rulings below decided what it says. They were not its ratification:
that is Brett Heap's own word on this exact text, and he gave it the same day,
in session to lane `openXfactory-5`, as a multiple-choice answer whose verbatim
option label is *"Ratify, OQs as recommended (Recommended)"* (see
[§ Ratification](#ratification) below). The word ratifies the packet as it
stood and adopts all six open questions of `design.md` at the recommended
answer, so the delta moved not one byte. It is a ratify word and nothing else.
The schema, validator and test work follows through one Speckit feature, which
the word now allows and which is no part of this pull request.

## The rulings this change carries

Brett Heap answered three multiple-choice questions on 2026-10-08, in session
to lane `openXfactory-5`. Each is RULED against this change path on the
estate's lane register (`opensoft/brett-wip`, `lanes/log/openXfactory-5.md`).
Each option label is quoted verbatim, followed by the option text as it read.

1. **"RS256 baseline (Recommended)"** (RULED 2026-10-08T18:36:55Z, commit
   `eed43d23`). The option read:
   > openxFactory's factory-mcp-conformance gets an auth block, and every
   > hosted domain server must accept RS256 (EdDSA optional). codexFactory
   > then adds RS256 in its own slice. That work also fixes the hosting plan's
   > pre-existing `issuer: hermes`.
2. **"Narrow to error codes (Recommended)"**, for M5 (RULED
   2026-10-08T18:37:07Z, commit `ceaa3c02`). The option read:
   > A MODIFIED requirement: a dependency failure reported through the error
   > inventory maps to an execution failure, which is already enforced, and a
   > red-first test pins it. Both real domains already model it this way.
3. **"Per domain, profile maps (Recommended)"**, for the error vocabulary
   (RULED 2026-10-08T18:37:19Z, commit `8534027e`). The option read:
   > Each domain keeps its codes and envelope; the profile's lossless mapping
   > is the only shared layer, stated in the same amendment as the auth
   > answer. No published schema changes.

## Ratification

**Brett Heap, 2026-10-08T20:2xZ, verbatim *"Ratify, OQs as recommended
(Recommended)"*.** He gave it in session to lane `openXfactory-5` as a
multiple-choice answer, and the lane recorded it as a RULED line on the
estate's lane register at 2026-10-08T20:33:25Z. The instant of the word is
written to the precision it was taken at and no finer, the form earlier
ratifications in this repository use. The full record is
[`review/ratification-2026-10-08.md`](review/ratification-2026-10-08.md).

Each open question of `design.md` carries its own RULED marker in the table
beside it. All six are RULED as recommended:

- **OQ-1.** Admit the `issuer_assigned` audience binding beside `resource_uri`.
- **OQ-2.** Keep the admitted algorithms closed at RS256 (required) and EdDSA
  (optional).
- **OQ-3.** Derive the metadata path by RFC 9728 § 3.1 insertion, and refuse a
  query on a hosted resource URI.
- **OQ-4.** The block cites evidence or a gap under a new `auth` concern.
- **OQ-5.** Keep `schema_version: 1` and `profile: advisory-v1`, and
  first-bundle the declaration at the next additive minor.
- **OQ-6.** Exactly one issuer per hosted server.

Every answer is the one the delta already encodes, so the ratification changes
no requirement or scenario text; the record shows each answer against the
delta line that carries it. Ratifying is not landing: this pull request stays
a draft, its landing takes a separate word under the Rule 6 landing window,
the realization follows through one Speckit feature, and the archive is a
later act on merged, green realization evidence and its own word.

## Why

**The profile has no authorization block.** The declaration schema carries a
deployed service's installation, environment and canonical resource URI, and
nothing about the tokens that server accepts. The realization of
`add-factory-mcp-conformance` ([#1243](https://github.com/opensoft/openxFactory/pull/1243))
left that item as "Not done … wait for rulings", and the archive record
repeats it. Under Brett Heap's 2026-10-05 ruling *"keep one server per
domain, no combined endpoint"*, every domain server faces the same estate
issuer, so the token profile belongs in the neutral capability, not in each
domain.

**The domains already disagree, and the disagreement fails at the first real
token.** Measured on 2026-10-08, at behaviour level:

- The engineering domain's hosted adapter accepts only EdDSA. Its own source
  records a second algorithm as an additive governed change (codexFactory,
  private, verified 2026-10-08).
- The estate's identity front door verifies RS256 tokens from its Entra
  issuer, and is never an issuer itself (xFactory-Hermes-Install, verified
  2026-10-08). Microsoft Entra ID cannot sign EdDSA.
- So the engineering adapter would refuse every token the estate's only live
  issuer signs.

**One ratified scenario cannot be enforced as written.** *Unavailable
dependency* asks that a domain unable to evaluate because a dependency is
unavailable map to "an execution failure and never eligible". The validator
classes each mapping row by its inventory alone: a value of an error
inventory must be an execution failure, and a value of a result inventory a
completed evaluation. It cannot tell what a result status means, so a result
status named for a dependency failure passes as a completed evaluation. Both
real domains report an unavailable dependency through an error code: the
operations domain's DNS check has only the result statuses `blocked` and
`eligible` (OpsxFactory, verified at its `main` on 2026-10-08), and the
engineering domain's published domain-error schema carries an
unavailable-dependency code (codexFactory, private, verified 2026-10-08). Narrowing the scenario to the error inventory
makes canon say what is enforced.

**Nothing records where the error vocabulary lives.** Each domain publishes
its own codes and envelope. Some code names recur across domains with
different envelopes and retry semantics. With one server per domain, no
client sees two domains' errors through one endpoint, and the profile already
normalizes what does cross domains: failure versus evaluation, and isError.

## What Changes

One delta, `specs/factory-mcp-conformance/spec.md`: FOUR `## ADDED`
requirements and ONE `## MODIFIED` requirement.

- **ADDED *Hosted declarations carry an authorization block*.** A deployed
  service's declaration carries a block naming the issuer, the accepted
  algorithms, the audience and its binding, and the protected-resource
  metadata path (RFC 9728). A declaration that is not deployed carries none:
  a server reached only over stdio takes its credentials from its host
  environment. The issuer is an absolute https issuer identifier without
  query, fragment or userinfo, never a runtime name. A hosted canonical
  resource URI carries no query. The block holds no key material and cites
  evidence or a gap.
- **ADDED *RS256 token-signing baseline*.** Every hosted domain server accepts
  RS256. EdDSA is an optional addition. `none` and HMAC are refused by name,
  and any other algorithm is a governed change to this capability.
- **ADDED *Audience bound to the server's own resource*** (RFC 8707 § 2).
  Exactly one audience, bound to the canonical resource URI or to an
  identifier the issuer assigns to this resource alone. Sharing an issuer
  never makes tokens interchangeable between domain servers.
- **ADDED *Per-domain error vocabularies*.** Each domain keeps its own codes
  and envelope. The lossless mapping is the only shared layer, and no
  published schema has to change.
- **MODIFIED *Lossless results and explicit failures*.** Title unchanged. Two
  edits, and the rest of the block is carried byte for byte:
  - the body gains the sentence *"Result-schema statuses SHALL map to
    completed evaluations, and error-inventory codes SHALL map to execution
    failures."*, and its eligibility sentence is narrowed to *"inability to
    evaluate that the domain reports through its error inventory"*;
  - the *Unavailable dependency* scenario's WHEN becomes *"the domain reports
    through its error inventory that it cannot evaluate because a dependency
    is unavailable"*. Its THEN and its title do not change, and neither do the
    other two scenarios.

`design.md` gives the block's shape, the validator's stable codes, the
contract version and six open questions, each with a recommended answer.
`tasks.md` lists the realization tasks and the downstream acts this change
does not perform.

## What this change does NOT do

- **It writes no schema, validator, test or runbook byte.** That is the
  realization, through one Speckit feature after the ratify word.
- **It cuts no contract release and reserves no number.** The cut is
  realization work under its own claim of row 4 on #630.
- **It changes no domain's published schema and adds no neutral error code.**
- **It does not amend codexFactory.** The engineering domain adds RS256 in its
  own governed slice (lane `openXfactory-5`). Until that slice lands, a hosted
  engineering declaration fails this profile's RS256 rule. That is the
  intended signal. Its stdio declaration is not deployed and is unaffected.
- **It does not correct OpsxFactory's hosting plan.** The approved hosting
  plan names its token issuer by a runtime name rather than an issuer
  identifier. Correcting it is a material plan amendment in OpsxFactory, with
  a fresh task 4.2 approval. This change only supplies the rule that
  correction meets.
- **It does not align the Ops gateway's intake.** That is lane
  `opsXfactory-4`'s, at gateway base task 3.1.
- **It runs no server, adds no transport package and mints no token.** The
  shared-transport trigger is untouched.
- **It does not edit the archived packet** of `add-factory-mcp-conformance`.
  An archive is the record of what was ratified.

## Impact

- **Affected spec:** `factory-mcp-conformance` (promoted). Four requirements
  are added and one is modified. The other seven are untouched.
- **Affected code, at realization:** the code surface named in the
  front-matter, all in openxFactory.
- **Affected gates when this packet lands:** the `modified-block-currency`
  family reports the MODIFIED block once, at INFO, because the block does not
  carry two of the ten units canon states for it: the eligibility sentence and
  the WHEN bullet, both narrowed. `tests/doc-health/test_modified_block_currency_self_gate.py`
  `_LEDGER_SUBJECTS` names the finding with one data row, which retires when
  this packet archives. The sweep ledger moves this change's row and flips
  `add-factory-mcp-conformance` from `sole` to `co-modifier`.
- **Downstream:** see `tasks.md` § 5.
