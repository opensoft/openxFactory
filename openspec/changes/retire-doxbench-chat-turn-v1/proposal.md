---
code_surface: openxFactory. (1) `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml` — RELEASE-SURFACE INVENTORY MEMBER **and** digest-pinned in `contracts/manifest.yaml` at `sha256: 2ff5f222af5cdccd545417203898a919be0365cdd0d2d5138e87e23f7ebfe1cf`: the `$defs/request`, `$defs/success` and `$defs/failure` blocks, their three `oneOf` refs at `:58-60`, and the whole top-level `deprecated_envelopes` block at `:70-82` with its explanatory comment at `:64-69` are REMOVED; the shared definitions the v1 envelopes `$ref` (`content_hash`, `confined_path`, `scope_key`, `buffer_state`, `transcript_turn`, `typed_proposal`) are RETAINED, being reachable from the surviving family, and each retention is measured from the surviving family's own reference closure rather than assumed. (2) `scripts/validate-ideation-dashboard-contracts.py` (member) — the three v1 rows in the kind→schema map at `:144-146`, the three tag-dispatch arms at `:392-397`, the paired-family kind tuple at `:1561-1562`, and whatever of the `deprecated_envelopes` reader at `:309-345` has no remaining subject. (3) `contracts/manifest.yaml` (member) — the schema's `sha256` moves, and the row prose at `:1681` onward drops its v1 clauses. (4) `contracts/README.md` (member) — the long row at `:86`. (5) `contracts/CHANGELOG.md` (member) — the `contract-v3.0` BREAKING entry. (6) `docs/contract-versioning-policy.md` (member) — the entry moves to § Deprecations Executed. (7) A new `contracts/releases/contract-v3.0.digests.yaml`. NON-MEMBER code and assets: `scripts/ideation_dashboard/serve.py` — the three v1 kind constants at `:377-379`, the kind-discrimination branch at `:3541-3558` INCLUDING ITS REDESIGNED FALLBACK, the v1 success builder `doxbench_turn_success_body` at `:1025-1059`, the v1 defaults on `doxbench_turn_failure_body` (`:954-957`) and `_refuse_turn` (`:3277-3279`), the v1 parser `_parse_workbench_chat_turn_body` (`:3450-3462`), and ONE NEW ENTRY in the closed `DOXBENCH_ERROR_CATALOG` for the unknown-kind code; `scripts/ideation_dashboard/doxbench_contracts.py:265-267`; TWELVE packaged fixtures under `examples/ideation-dashboard/` (four positive `.example.yaml` and EIGHT under `negative/`); `examples/ideation-dashboard/README.md:307-313`; `tests/ideation-dashboard/fixtures/chat-turn-v1-envelopes.baseline.yaml` and the byte-identity assertion at `tests/ideation-dashboard/test_doxbench_contracts.py:1213-1239`; and seven further test files across BOTH directory spellings (`tests/ideation-dashboard/` and `tests/ideation_dashboard/`). NO change to the surviving `-v2` family's shape: not one field is added, removed or renamed by this removal.
target_release: contract-v3.0 — a MAJOR, and naming it is not the reservation the policy forbids: § Version Identity forbids reserving a MINOR before merge order is known, and the major is deterministic from the declared bundle (`contract-v2.5`) and already named as a forward target by the In Force entry `add-binding-consumer-identity` landed 2026-08-31. THIS CHANGE HAS A CODE SURFACE AND MOVES SCHEMA BYTES, so under `release-realization` it archives ONLY on merged plus green realization evidence — never on landing — and the evidence includes the moved manifest digest, the rebuilt inventory, and the published annotated `contract-v3.0` tag verified from an independently refreshed checkout. The cut is a SEPARATE act from this proposal and from its realization.
Status: draft
Proposed: 2026-09-01
Origin: openxFactory issue #522, entry 3 of three; measured 2026-08-31 in a decision memo durable on the operator host at `~/projects/xFactory/deprecations-522-memo-2026-08-31.md`; RULED by Brett Heap 2026-09-01 in session and recorded as a comment on #522 — "execute all three retirements at contract-v3.0, as the memo recommends", entry 3 "EXECUTE, its own slice", with the `serve.py` v1-fallback posture "redesigned, not deleted". The ruling authorizes the proposal; it does not ratify this text.
---

# Proposal: retire-doxbench-chat-turn-v1

## Why

**This is the one deprecation in the estate whose warning actually fires, and it
has been naming a spent target on every default validator run for five minors.**
Run today over a clean checkout:

```
validate-ideation-dashboard-contracts: 0 error(s), 4 warning(s)
```

all four reading *"removal target contract-v2.0"* — a target the bundle passed on
2026-08-27, one major and five minors ago. Nothing checks that sentence, so
nothing noticed.

**The deprecation was done properly and then not finished.** `contract-v1.34`
introduced the widened `-v2` family as a CO-RESIDENT one rather than by mutating
a closed envelope, kept the v1 bytes byte-identical to their `contract-v1.31`
bytes and committed a baseline test to prove it, and declared the deprecation
MACHINE-READABLY — a top-level `deprecated_envelopes` block carrying
`superseded_by`, `deprecated_in: contract-v1.34` and `removal_target:
contract-v2.0` per kind, written outside every envelope precisely so the
deprecated bytes would not have to move to say they were deprecated. Every
obligation of the *Deprecating (minor)* class was met. The one act left — the
removal at the major it named — was not performed, and `contract-v2.0` shipped
without looking.

**A co-resident family that is never removed is not a deprecation; it is a
second contract.** Two envelope families are served, two parsers are maintained,
two failure paths exist, and one of them is answered by nobody: the shipped
browser client sends `-v2` kinds exclusively, and there is no v1 emitter
anywhere in the estate.

Cited in full: openxFactory issue **#522** and Brett Heap's ruling comment on it
of **2026-09-01**; the measurement memo
**`~/projects/xFactory/deprecations-522-memo-2026-08-31.md`**.

## What the measurement found, and where it did not survive re-verification

Re-measured on this branch against main tip `1a69b7cb`. **The memo's shape holds
and its PRICING was low in two places.**

**Confirmed.** Zero v1 emitters (the shipped client at
`scripts/ideation_dashboard/web/views/doxbench-chat.js:37-39` is `-v2`-only);
zero v1 instances outside openxFactory's own packaged fixtures; the schema's
`deprecated_envelopes` block at `:70-82`; the machine-readable deprecation read
by the validator at `:309-345`; the four warnings, reproduced above verbatim.

**CORRECTION 1 — the packaged corpus is TWELVE fixtures, not four.** The memo
counted the four positive `.example.yaml` files, which are the four the default
run warns on. It missed the **eight NEGATIVE fixtures** that also declare v1
kinds:

| refusal class | fixture | v2 equivalent? |
| --- | --- | --- |
| escaping path | `negative/workbench-chat-turn-escaping-path.negative.yaml` | none |
| hash mismatch | `negative/workbench-chat-turn-hash-mismatch.negative.yaml` | none |
| identity subject | `negative/workbench-chat-turn-identity-subject.negative.yaml` | none |
| over budget | `negative/workbench-chat-turn-over-budget.negative.yaml` | none |
| unknown model | `negative/workbench-chat-turn-unknown-model.negative.yaml` | none |
| untyped proposal | `negative/workbench-chat-turn-untyped-proposal.negative.yaml` | none |
| duplicate turn pair | `negative/duplicate-turn-pair/turn-a.yaml`, `turn-b.yaml` | none |

The surviving family has its own ten negatives, and they cover a DIFFERENT set —
context-packet posture, reserved key path, unbound buffer, provider-retry token
leakage. **Seven refusal classes are carried by v1 negatives alone.** Retiring
the family without re-expressing them against `-v2` silently deletes seven
refusals from the packaged corpus. That is the single largest thing the memo's
pricing missed, and § What Changes carries it as an explicit obligation rather
than an assumption that "the fixtures go with the family".

**CORRECTION 2 — there are TWO fallback layers, not one.** The memo named the
kind-discrimination fallback (`serve.py:3541-3558`). Underneath it,
`_refuse_turn` (`:3277-3317`) has its own: when the request carries no wire-valid
turn identity, or when the built envelope fails its own self-validation, the
route drops out of the contract envelope entirely and answers in
`doxbench_error_body`'s fixed pre-identity shape. That second layer is NOT
removed and NOT redesigned by this change — it is the correct answer for a
request with no identity, and the surviving failure envelope requires a
`client_turn_id` that no server may invent. Naming it matters because a redesign
that ignored it would either duplicate it or break the no-invented-identity rule.

**Confirmed and sharpened — the fallback CAN be redesigned onto the surviving
family.** `$defs/failure_v2` requires `schema_version`, `kind`, `client_turn_id`,
`error`, `message`, and constrains `error` by a lowercase-identifier PATTERN
only. There is no enum at the schema layer, and the delegated validator that
judges a v2 failure is the SAME function that judges a v1 failure and applies no
code vocabulary either. The only CLOSED list is `serve.py`'s own
`DOXBENCH_ERROR_CATALOG`, which maps code to status and to a fixed message and
raises on an unregistered code. An explicit unknown-kind code is therefore
contract-permitted today and needs one catalog entry, not a schema widening.

## The design question this change must answer, ANSWERED

**Question.** Today an unrecognized or absent chat-turn `kind` is coerced into
the **v1** family: `serve.py:3554-3557` forces `request_kind` to the v1 request
kind, sets `failure_kind` to the v1 failure kind, and selects the v1 parser. The
comment states the reason — *"a request that never named a family it could be
answered in gets the posture it would have got before this release"*. Removing
v1 destroys that reason and, taken literally, would leave the `else` branch
dispatching to a parser and an envelope builder that no longer exist. **What
replaces it?**

**ANSWER, and it is a decision this proposal takes rather than leaves open:**

> An unrecognized or absent `kind` is answered in the **surviving `-v2` failure
> envelope**, carrying an **explicit unknown-kind error code** registered in the
> server's error catalog, whenever the request carries a wire-valid
> `client_turn_id`. Where it does not, the existing **pre-identity refusal
> shape** answers, unchanged — because `failure_v2` requires a `client_turn_id`
> and the route's standing rule is that it *"never invents a turn identity"* to
> reach a contract envelope.

**Why this and not the alternative.** The alternative is to refuse every
unrecognized kind OUTSIDE any contract envelope — the pre-identity shape for all
of them, whatever identity the request supplied. It is simpler and asserts less,
and it is recorded here rather than left unsaid. It is not taken because it pays
three costs to avoid registering one error code: it discards an identity the
request DID supply; it hands the client a body carrying no `kind` its own
dispatch can route, on a rail whose client dispatches on exactly that; and it
makes the refusal invisible to the contract corpus, so no packaged fixture can
ever cover it.

**What makes the chosen answer legal on the contract as it stands** is measured
above: `error` is pattern-constrained and not enumerated, at the schema layer and
at the validator layer both. No schema widening is needed, and none is proposed —
the only schema movement in this change is REMOVAL.

## What Changes

- **REMOVE the three v1 envelope kinds at `contract-v3.0`** — their `$defs`,
  their `oneOf` refs, the `deprecated_envelopes` block, the runtime and
  validator dispatch, and the packaged instances.
- **RETAIN every shared definition the surviving family reaches**, measured from
  its own reference closure. Only definitions reachable from the removed
  envelopes ALONE may go.
- **REDESIGN the unrecognized-kind posture** as answered above, with one new
  entry in the closed error catalog.
- **Re-express or explicitly record the seven v1-only refusal classes.** Each
  either gets a `-v2` negative fixture or a stated coverage loss with a reason.
  Neither is optional and silence is not one of the choices.
- **Retire the byte-identity baseline test by naming what it was for**, not by
  deleting a file: it exists to prove the deprecated bytes never moved, and it
  ends because the shape it protects leaves the published surface.
- **Move the entry to § Deprecations Executed** with all six elements the one
  exemplar row establishes, so the migration path stays readable at the version
  a consumer is upgrading TO.
- **Repair `examples/ideation-dashboard/README.md:307-313`**, which tells the
  reader `--strict` will keep failing *"until the removal target contract-v2.0
  retires the fixtures with the family"* — false since 2026-08-27, in exactly
  the silent way this whole issue is about.

## What this change does NOT do

- **It does not cut `contract-v3.0`.** That is its own act under § Bundle
  Realization Order.
- **It does not touch the surviving `-v2` family's shape.** Not one field.
- **It does not touch the `hermes` flat keys or the `openworkflow_` tokens.**
  That is the sibling packet, and the two are independent: this delta touches
  only `ideation-dashboard` and does not depend on the capability the sibling
  adds.
- **It does not remove the pre-identity refusal layer**, which is correct and
  stays.

## Capabilities

### Modified Capabilities

- `ideation-dashboard`: **TWO ADDED requirements** — the removal itself, and the
  unrecognized-kind posture — and **ONE `## MODIFIED Requirements` block** over
  the promoted requirement "The chat-turn contract release carries the bound
  buffer and the model", which is the only promoted requirement that governs the
  deprecated family's survival.

**THE MODIFIED BLOCK IS SCENARIO-COMPLETE AND CARRIES EVERY CANON UNIT.** All
four of canon's scenarios are restated — "An older client sends a released v1
turn", "The release version is reserved early", "A record is asked which model
answered", "A field has no room in the envelope" — with every bullet of each, and
the body paragraph carried verbatim. **Nothing is dropped**, so the block needs
no `Removed from canon` marker and declares none; the amendment is by ADDITION
of three body paragraphs and three scenarios that BOUND the survival obligation
to the removal target the same release recorded, rather than by striking the
obligation that was in fact discharged.

**#538's base-declaration convention does not apply.** `Modified over` governs a
MODIFIED block whose requirement exists only as an active sibling's `ADDED`. This
block's requirement is in PROMOTED canon at
`openspec/specs/ideation-dashboard/spec.md:2178`, so the family resolves it
against canon and the pairing class is never reached. The sibling packet carries
no MODIFIED block at all, so there is no pair to declare in either direction.

## Impact

- **Refuses no consumer.** No v1 emitter exists in the estate; the dashboard is
  openxFactory-internal and its only shipped client is `-v2`-only.
- **The largest release surface of the three entries.** Six inventory members
  move, including a digest-pinned schema whose `sha256` changes and an inventory
  that rebuilds.
- **Test surface:** eight test files across two directory spellings, plus the
  baseline fixture. The byte-identity assertion at
  `test_doxbench_contracts.py:1213-1239` is retired deliberately.
- **The measurement boundary the memo stated is inherited and restated:** no
  doxBench client outside the ten measured repositories is visible from here. The
  in-repo client is `-v2`-only and the risk is assessed low, but it is an absence
  of evidence and is named as one. **If a pinned external v1 client exists, this
  becomes record-why-it-stays until it migrates** — and, under
  § Compatibility Direction, such a client stays valid at its pin regardless.

## Orchestrator Decisions

**D1 — the unrecognized-kind posture is the surviving family's failure envelope
with an explicit code.** Stated and argued above. *Alternative recorded:*
envelope-less refusal for all unrecognized kinds.

**D2 — the seven v1-only refusal classes are re-expressed or their loss is
stated.** No third option. A retirement that quietly reduces the negative corpus
is how a refusal stops being tested without anyone deciding it should.

**D3 — the shared `$defs` are retained by MEASUREMENT, not by inspection.** The
realization computes the surviving family's reference closure and removes only
what falls outside it. The existing baseline test's own closure computation is
the model.

**D4 — the baseline test's retirement is named in the changelog entry.** A test
whose stated purpose is "prove the deprecated bytes never moved" cannot be
deleted as collateral without the record reading as though it became
inconvenient.

**D5 — this packet is separate from the sibling and depends on none of it.**
Both target `contract-v3.0`; either may be cut alone. This delta deliberately
adds its requirements to `ideation-dashboard` rather than to the sibling's new
`contract-deprecation-execution` capability, so that this packet's obligations
stand on their own text whether or not the sibling is ratified.

## Open Questions

- **OQ-1 — does `contract-v3.0` carry both retirement packets, or one?** The
  cutting session's decision, not this proposal's.
- **OQ-2 — is `contract_schema_version` incremented?** § Version Identity says
  major increments occur together with it. This change DOES move a schema's
  bytes, so it meets the question more directly than the sibling does; the answer
  belongs to the cut.
- **OQ-3 — what is the unknown-kind code's exact token and HTTP status?** The
  contract constrains only the pattern. The realization picks both and registers
  them; this proposal deliberately does not name a token it would then have to
  defend against the catalog's existing naming.
- **OQ-4 — is an external doxBench client pinned to v1?** The one measurement
  the memo wanted and could not perform. It is not blocking on the evidence
  available, and the honest consequence if the answer is yes is stated in
  § Impact.
