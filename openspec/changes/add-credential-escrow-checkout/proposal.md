---
code_surface: openxFactory — A SCHEMA CHANGE PLUS PACKAGED FIXTURES, widened from fixtures-only when Brett VETOED OD-2 on 2026-08-28. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains TWO ADDITIVE THINGS: an optional `escrow:` block on the existing `xfactory_credential_binding_template` (naming the escrow entry, the escrow scope, and the MUST/SHOULD classification with its retained authority), and a SIXTH record kind `xfactory_credential_escrow_entry` (source, runtime target, escrow artifact with encrypted FIELD NAMES, restore target and validations) shaped on the running prior art at `Opensoft-Tenant-openxpki-qa` `escrow/**/inventory.yaml` and `restore-map.yaml`. `scripts/validate-credential-contracts.py` gains the sixth kind and the optional block. PLUS the packaged conformance fixtures under a new `contracts/credentials/examples/` tree: the four checkout records built from already-promoted kinds (escrow-identity requirement, custody binding, time-boxed checkout grant template, break-glass audit policy declaring the decrypted-object enumeration among its `minimum_fields`), a binding carrying an `escrow:` block, an escrow entry, and the negative fixtures for every named refusal (a runtime decryption-controller recipient reused as an escrow recipient; a checkout grant with no recorded human-and-domain approval; an audit policy omitting the enumeration; a SHOULD-escrow classification naming no retained authority; an escrow discriminator added to a custody axis; an entry carrying a value; an entry with no restore target), registered in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`. NO change to any `contracts/trust-anchor/` file, as that change's OQ2 ruling promised. NO registry, no inventory-completeness obligation, no drift audit, and no decryption-free lint — ruling C's home and grandfathered exception and the lint stay with the successor (OD-3, CLEARED as authored). The Client Hermes realization (the escrow identity's records under `config/clients/opensoft/credentials/`, the recipient establishment, and the recorded drill) lands in `xFactory-Hermes-Install` and is a successor-repo realization, not this repository's surface. SEPARATELY AND AT AUTHORING, this packet edits `tests/doc-health/test_modified_block_currency_self_gate.py` to register its MODIFIED block as a named carriage-ledger subject — a bookkeeping consequence of carrying a MODIFIED block at all, required by that gate in the same commit as the block, and not part of the realization surface described above.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. `contract-v2.0` is the declared bundle (`contracts/manifest.yaml:3`) and the active packet `fix-content-resolution-conflation` is realizing the next minor in parallel, so a number written here would be a number another packet is already spending; the `contract-v1.28` renumber sweep is the standing precedent for why a proposal must not spend a minor before merge order is known. **A CUT IS NOW OWED, AND THE MECHANISM MATTERS BECAUSE IT IS NOT THE OBVIOUS ONE — MEASURED, NOT ASSUMED.** Parsed here on 2026-08-28: `contracts/releases/contract-v2.0.digests.yaml` holds 192 entries and `contracts/schemas/xfactory-credential-contracts.schema.yaml` IS NOT ONE OF THEM — only five `contracts/schemas/` files are members, all `release-schema` type, none of them this one. The release membership closure is built from `contracts/hermes-runtime/contract-index.yaml` entries marked `release_member` (`scripts/hermes_runtime_validation/release.py:453-500`, `CATALOG_PATH` at `:38`), and that catalog carries no credential entry. **So the cut is NOT forced by release-inventory-drift**, which is the usual reason a schema edit owes one. It is owed by the VERSIONING POLICY instead: the schema is a registered bundle contract (`contracts/manifest.yaml:2079-2094`, `id: credential-contracts`), and a registered contract gaining a record kind and an optional field is the policy's ADDITIVE (MINOR) class verbatim — "new optional fields, new contracts" — under which "Domain repos on the same major version remain conformant without changes". Registering the fixtures edits `contracts/manifest.yaml`, which IS a digest-inventory member but is one of exactly three EDITORIAL members permitted to move between cuts (`scripts/doc_health/release_inventory.py:62-66`). THE CLASS IS ADDITIVE AND NOTHING NARROWS: a binding template declaring no `escrow:` block stays valid, a repository holding no escrow entry stays conformant, `contract_schema_version` is unchanged, and every consumer pinned at `contract-v2.0` stays conformant until it upgrades — which is why the MODIFIED block states that property as its own two scenarios. THE ARCHIVE GATE IS MERGE PLUS GREEN PLUS THE CUT PLUS ONE REHEARSED DRILL: Brett's ruling D makes the drill the gate, and the same drill discharges `deployment-handoff-boundary`'s phased-never-gapped milestone.
Status: ratified
Ratified: 2026-08-28 by Brett Heap — four multi-choice selections, each taking the orchestrating session's recommended option, over a read-only decision round on `ideation/staging/client-credential-escrow-registry/`. The four rulings are recorded verbatim in `.openspec.yaml` and restated in § What Brett ruled below. THE CITATION COVERS THE FOUR RULINGS AND THE ADMISSION OF THIS PACKET INTO THE QUEUE, AND NOTHING ELSE. It does NOT cover this packet's requirement text, the proposed policy-window numbers, or the decision to carry no schema surface in this first packet; those are the authoring session's and are flagged for veto in § Orchestrator decisions. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctions for exactly that case, and clears its three-way floor: approver (Brett Heap), date (2026-08-28), and a resolvable record path (this file, § What Brett ruled, and this packet's `.openspec.yaml`). **A SECOND ACT LATER THE SAME DAY CLOSED THE VETO WINDOW AND CHANGED THIS PACKET'S SHAPE.** All seven § Orchestrator decisions were ruled and all five § Open Questions answered on 2026-08-28, by a four-question multi-choice put to Brett by the orchestrating session over pull request #479 and relayed the same day. **OD-2 was VETOED** — the escrow relationship block and the escrow-entry record kind come into THIS packet on ruling A's literal shape, and Brett accepted the stated consequence that realization now owes the additive contract cut. OD-4 was APPROVED as authored (24 hours / 5 business days, non-tolling, lateness-is-a-finding). OD-1, OD-3, OD-5, OD-6 and OD-7 were CLEARED as authored, with OD-3's deferral of ruling C's home, grandfathered exception and escalation tests to the successor expressly STANDING — only the schema half moved here. FOUR of the five open questions were ruled on this packet's own recommendations and **OQ5 was ruled AGAINST IT** — the drill must ALSO prove a LIVE refusal, where the packet had recommended proving refusals by fixture alone; the reversal is recorded as a reversal rather than smoothed into agreement. Merge on green was approved, to be performed by the orchestrating session rather than this one; realization is a later commission, because the drill needs Brett's hands on real material. THE TWO ACTS STAY DISTINCT ON PURPOSE: the first ADMITTED the packet and ratified four positions, the second CLOSED the veto window and MOVED DELTA TEXT — which is the difference from the sibling precedent where a clearance moved none.
Proposed: 2026-08-28
Origin: Staged topic `client-credential-escrow-registry` (staged 2026-07-19 from Brett's track-1 QA secret-custody design), raised to EXIT 1 OF TWO by Brett's split ruling D of 2026-08-28. The split is not in the staged topic — its own Exit names one change carrying the whole registry — so the origin act is the ruling, and the topic stays staged for the successor with its `INDEX.md` row updated in this packet's commit. The immediate forcing fact is not the topic but a live obligation: the opensoft QA install already reads `execution_binding.mode: opsxfactory_executed` at `status: completed` and `config/clients/opensoft/credentials/` does not exist.
---

# Proposal: add-credential-escrow-checkout

## Why

**`deployment-handoff-boundary` is ratified canon with a hole in it that only
this packet can fill.** Its phased-never-gapped requirement
(`openspec/specs/deployment-handoff-boundary/spec.md:122-135`) holds the
operator's existing standing administrative access open as a named,
dispositioned exception "until the break-glass checkout path is realized and
tested", and its no-standing-credentials requirement (`:51-73`) already says
human direct access is "break-glass only: a time-boxed credential checkout with
evidence, followed by a retroactive request within the governing policy window".
Three things that sentence depends on were deliberately not written there. Who
may check out. What evidence the checkout leaves. How long the window is. That
change's design says so in as many words at `design.md:136-138`: "Who can break
glass, how credentials are custodied, and the window's length belong to
`client-credential-escrow-registry`." Until they are written, the exception
cannot close and the standing access cannot be removed — which is the exact
outcome the boundary was ratified to end.

**The escrow duty is live today and unmet.** Verified in the working checkout on
2026-08-28 rather than assumed: the opensoft self-client QA install's execution
binding reads `execution_binding.mode: opsxfactory_executed` with
`status: completed`
(`xFactory-Hermes-Install`
`config/clients/opensoft/requests/cir-opensoft-qa-codexfactory-transfer.yaml:65`
and `:83`; the transfer completed 2026-07-20), and
`config/clients/opensoft/credentials/` DOES NOT EXIST. Under the staged topic's
claim 6 — the one Brett named in 2026-07-19 — a managed install owes escrow as a
contract obligation. The install is managed. The registry is absent. That gap has
been open for five weeks with nothing recording it as a gap.

**And the operator has already been solving it by hand, correctly, in the wrong
place.** The `Opensoft-Tenant-openxpki-qa` install repository carries a working
escrow tree today: `escrow/**/inventory.yaml` and `restore-map.yaml` records with
`source.credential_requirement`, `runtime_target` and
`escrow.format: sops-age`; four `dr-escrow-*` scripts; a
`docs/dr-secret-escrow.md` runbook; and — this is the part worth noticing — two
age recipients in `escrow/recipients/age-recipients.txt` that are already
DISJOINT from the live QA Flux reconciler's recipient in
`Omnigent-Install/.sops.yaml`. The separation Brett ruled in B is not a new
constraint being imposed on practice; it is practice, unwritten, one operator
decision away from being lost.

## What Brett ruled, 2026-08-28

Four multi-choice questions, four selections, each taking the prep's
recommendation. Recorded here because three of the four bind this packet's text
and the fourth is why this packet exists at all.

- **A — Delta shape.** `credential-contracts` gains an additive optional
  `escrow:` relationship block on the existing
  `xfactory_credential_binding_template`, PLUS one new record kind for the escrow
  entry itself (inventory and restore target), shaped on the running prior art.
  The governing precedent is Brett's own trust-anchor ruling of 2026-08-21 —
  "operator escrow is a relationship on the credential record, not a custody
  tier" — whose executable form is the negative fixture
  `contracts/trust-anchor/examples/negative/custody-registry-escrow-as-a-custody-tier.yaml`.
  **This packet carries ALL of it.** As authored it carried none, on OD-2; Brett
  **VETOED OD-2 on 2026-08-28** over PR #479 and accepted the stated consequence
  that realization now owes the additive contract cut. Realized here as the
  MODIFIED block (the schema owns six kinds, not five) plus two ADDED
  requirements — the escrow relationship on the binding, and the entry shape.
- **B — Key topology.** Per-client recipient PLUS one operator root on every
  file; drills restricted to the per-client key; the escrow recipient set
  disjoint from every runtime decryption-controller recipient, so the live QA
  Flux age recipient may never be an escrow recipient. Honest cost recorded at
  the ruling: the root's worst-case radius is every client. **Realized here as
  the fifth requirement, both halves including the recorded cost.**
- **C — Registry home.** Client Hermes
  `config/clients/<client_ref>/credentials/` canonical; the openxpki install-repo
  escrow grandfathered as a named, dispositioned exception until migrated, on the
  phased-never-gapped device; three structural escalation tests, any one of which
  forces a dedicated registry repository. **Carried to the successor whole**
  (OD-3) — the home is a property of the registry, and this packet contains no
  registry.
- **D — Scope: SPLIT.** The checkout path first, so the standing-admin exception
  can close; the full registry follows as packet two. Two sub-confirmations:
  **this filing SETS the policy window** that `add-deployment-handoff-boundary`
  deferred here, and **the QA Flux deploy key is SHOULD-escrow** under the
  re-mint test, being regenerable while the operator holds GitHub organization
  ownership (`Omnigent-Install`
  `clients/opensoft/docs/qa-subscription-migration-handoff.md:159-162`: "PRIVATE
  half only in the track-1 session scratchpad — if lost, generate a new pair and
  update the deploy key + TF var"). **Both realized here**, the second
  generalized into a testable rule (OD-6).

## The policy window this packet sets — APPROVED as authored (OD-4, ruled 2026-08-28)

`add-deployment-handoff-boundary` left it as an open question in one line
(`design.md:219-221`): "how long after an out-of-band action the retroactive
request must land. Realization detail; the escrow topic may set it." There is no
numeric window precedent anywhere in this capability family — searched, not
assumed — so the number is derived rather than inherited.

**Proposed: OPENED within 24 hours; DISPOSED within 5 business days; both bounds
running from the checkout's expiry or revocation, neither tolling.**

**Why two bounds rather than one.** They are different acts with different costs.
Opening the record is unilateral, takes minutes, needs no counterparty, and is
transcribed from the audit record the operator is already holding — the
correlation identifier, the objects decrypted, the authorizing incident. Reaching
an accepted disposition needs a second party AND needs rotation to have
COMPLETED, and rotation of a credential on a client surface can need a change
window. One bound covering both either makes the fast act slow or makes the slow
act impossible, and a single bound set for the slow act leaves the change
uncorrelated for a working week — which is the failure mode the next paragraph is
about.

**Why the opening bound is 24 calendar hours, and why that number and not
taste.** It is set by the DETECTION mechanism.
`deployment-handoff-boundary`'s out-of-band detectability requirement makes an
observed change with no correlated request a first-class finding at the periodic
evidence-correlation audit. If the opening window is LONGER than the audit
period, every legitimate break-glass manufactures a finding that then has to be
retracted, and a finding that is usually noise stops being read — the audit is
destroyed by its own true positives. So the opening bound must sit under the
audit period. 24 hours sits under any plausible cadence for that audit, and the
act it bounds genuinely takes minutes. It is stated in CALENDAR hours, not
business days, precisely because it needs no counterparty: business-day framing
is borrowed from approval workflows, and importing it here would let a Friday
evening checkout go unaccounted until Tuesday for no reason connected to the
work.

**Why the disposition bound is 5 business days.** One working week is the
shortest bound that a rotation requiring a scheduled change window can actually
meet, and the longest that still lands the disposition inside the same
incident-review cycle rather than deferring it into folklore. Business days here
because this bound DOES have a counterparty.

**Why the window does not toll, and where waits go instead.** The
`client_infrastructure_request` contract already models this correctly and the
window should not invent a second mechanism: its `conditions` array is documented
as "orthogonal to `status`: overdue / escalation / holds coexist with the
workflow state and are never expressed as a status value", with `overdue` and
`awaiting_external_response` among its members
(`contracts/schemas/xfactory-client-infrastructure-request.schema.yaml:234-255`).
A wait is therefore a condition, visible, with a `policy_ref` and clearing
evidence — not an extension that makes the bound unfalsifiable.

**Why lateness does not void the account.** A late filing still correlates the
change, which is the thing the audit needs; the lateness is recorded as its own
separate finding. The alternative — treating a late request as no request —
creates an incentive to file nothing once the bound has passed, and buys a
cleaner rule at the cost of the record.

This was OD-4, flagged for veto as authored on the grounds that Brett ruled a
window be set but not what it should be. **RULED 2026-08-28 over PR #479:
APPROVED exactly as authored** — 24 hours to open, 5 business days to dispose,
non-tolling, lateness-is-a-finding. Nothing in this section moved at the ruling;
it is reproduced as it stood.

## What this changes

**Ten requirements on `credential-contracts` — nine ADDED and one MODIFIED — and
46 scenarios (38 under ADDED, 8 in the MODIFIED block).** As authored this was seven ADDED, 28 scenarios and no MODIFIED
block anywhere; the OD-2 veto added requirements 8 and 9 and forced the MODIFIED
block, because a promoted requirement that enumerates FIVE record kinds becomes
false the moment a sixth exists.

**MODIFIED — Canonical credential record shapes.** The surgical change canon
requires and nothing more: five kinds become six,
`xfactory_credential_escrow_entry` joins the enumeration, and a closing paragraph
states that both additions are additive and narrow nothing. Two of the six
promoted scenarios say "five" in their own text and are amended to "six" — the
only promoted words that move — and two scenarios are added to pin the additive
property itself: a binding predating the block still validates, and the sixth
kind is a contract record rather than a domain policy record skipped with notice.

1. **Break-glass escrow checkout is an administration-tier custody act.** The
   escrow decryption identity is itself a credential, so the checkout is the
   already-ratified administration-tier custody shape
   (`roles-authority-model:166`) applied to a new credential class: requirement,
   binding, time-boxed scope-named grant, audit record per action with an
   evidence reference. Human AND domain approval before issuance. A client-layer
   credential steward — a role holding references and never secrets — cannot be
   the authorizing authority. And routine escrow WRITING never needs a checkout,
   because encryption needs only the committed public recipient.
2. **A break-glass checkout leaves three correlated records.** The retroactive
   request, the credential access audit record ENUMERATING EVERY object
   decrypted, and the authorizing incident or drill record — one correlation
   identifier across all three. The enumeration is carried by the promoted
   `xfactory_credential_audit_policy`'s `minimum_fields`, so it is a contract
   obligation rather than prose. No new request kind: the retroactive request is
   a `client_infrastructure_request` (`request_type: remediation`), because the
   boundary already ruled that a crossing does not get its own kind.
3. **The two-bound policy window**, above.
4. **After-use rotation covers every credential decrypted** — the enumeration is
   the worklist, reachable-but-not-decrypted is deliberately excluded, and the
   escrow identity itself rotates only where its private half left approved
   custody onto a non-ephemeral host; when it did, the promoted exposure rule
   applies unmodified.
5. **Escrow recipients are disjoint from runtime decryption controllers**, with
   the two-recipient floor, drills restricted to the per-client key, and the
   operator root's every-client radius recorded as an accepted cost.
6. **A rehearsed drill is the realization gate**, defined by what it exercises so
   a walkthrough cannot pass for one, and discharging two gates with one act. It
   must ALSO demonstrate at least one LIVE REFUSAL — added on OQ5's ruling
   AGAINST this packet's own recommendation — because a path never observed to
   refuse has been shown to work and not shown to govern.
7. **The re-mint test decides MUST-escrow from SHOULD-escrow**, with the
   named-retained-authority condition that makes a SHOULD classification
   falsifiable.
8. **The escrow relationship rides the credential binding, never a custody
   tier** (added at the OD-2 veto). The optional `escrow:` block is the only
   place a credential's escrow relationship may be expressed; it names the entry,
   the scope, and the classification with its retained authority; and no custody
   or assurance axis may carry an escrow discriminator. This is Brett's
   trust-anchor ruling applied where it pointed, and the family already holds the
   executable proof of the alternative's cost — the negative fixture in which an
   escrow member is forced to declare exactly the same two booleans as the member
   above it, because the escrow fact is invisible to that axis.
9. **The escrow entry records what was escrowed and where it restores** (added at
   the OD-2 veto). Source, runtime target, escrow artifact with its encrypted
   FIELD NAMES, restore target and validations — shaped on the prior art rather
   than invented. Every field is non-secret metadata, which is the property that
   makes the successor's decryption-free lint possible at all: field names are
   metadata, field values are not, and an entry naming a value has become the
   thing it exists to avoid. Where the runtime store holds a derivative, the
   entry holds the recoverable value — a hash restores nothing.

## What this deliberately does not change

- ~~**No schema.** `contracts/schemas/xfactory-credential-contracts.schema.yaml`
  is byte-unchanged. Ruling A's `escrow:` block and escrow-entry record kind are
  the successor's, whole (OD-2).~~ **REVERSED BY THE OD-2 VETO, 2026-08-28.**
  Both come into this packet on ruling A's literal shape, the schema is now this
  packet's surface, and realization owes the additive cut. The struck text is
  kept because the veto is only readable against what it overturned.
- **No trust-anchor file.** That change's OQ2 ruling promised "no change to any
  schema here" when it deferred escrow to this topic, and the promise is kept.
- **The SOPS ciphertext requirement is CITED, NOT RE-LEGISLATED.** Its six
  controls already make committed SOPS ciphertext not-a-raw-credential, and its
  exposure-triggers-rotation clause is exactly the rule requirement 4 defers to
  rather than restating. Requirement 5 is that requirement's own
  "recipients are unique per environment or stronger trust boundary" clause
  applied — escrow being the stronger boundary — not a competing rule.
- **No delta on `deployment-handoff-boundary`.** Measured, not assumed: its
  promoted text already references the checkout path and the policy window as
  things owned elsewhere, so this packet SUPPLIES what that text points at. A
  MODIFIED block there would restate its requirement to add nothing (OD-5).
- **No delta on `roles-authority-model`.** Its administration-tier custody
  requirement is applied to a new credential class, which is what a neutral
  requirement is for.
- **No registry, no inventory obligation, no drift audit, no validator.** All
  packet two's.

### Named follow-ups, out of scope here

- **Two incompatible `vaultref://` grammars.** `xFactory-Hermes-Install`
  `config/runtime-manifest.schema.yaml:236` accepts
  `^(env:|file:|vaultref://|k8s-secret://|azure-keyvault://|secretref://)[A-Za-z0-9_./:+-]+$`;
  `Omnigent-Install` `schemas/worker-host-manifest.schema.yaml:361` accepts
  `^vaultref://kv-[a-z0-9-]+/secrets/[A-Za-z0-9-]+$`. The first is a strict
  superset of the second, so a reference valid in the install repo is valid in
  Hermes and not conversely — meaning any completeness audit phrased as "every
  `vaultref://` has an escrow entry" silently depends on which grammar it parses.
  **The mitigation is already in the successor's shape**: scope any drift audit to
  DECLARED escrow entries, so it never has to parse either grammar. Reconciling
  the two is a cross-repo follow-up owned by neither packet.
- **The openxpki escrow tree's migration** to the canonical Client Hermes home,
  under ruling C's grandfathered exception. Successor.
- **Live refuse-then-allow proof** for the authorization refusals: the neutral
  layer holds no grant issuer, so this packet's refusals are proven by fixture
  here and at a domain mint surface later — the same shape
  `credential-contracts`' own roster-drift precondition already uses and states
  in its promoted scenario.

## Orchestrator decisions — ALL SEVEN RULED 2026-08-28 (authored: flagged for veto)

**The mechanism, recorded rather than paraphrased.** The orchestrating session
put four questions to Brett as multi-choice over pull request #479 and relayed
the answers the same day. **OD-2 was VETOED. OD-4 was APPROVED as authored.
OD-1, OD-3, OD-5, OD-6 and OD-7 were CLEARED as authored**, with OD-3's deferral
expressly standing. Four of the five open questions were ruled on this packet's
own recommendations and **OQ5 was ruled against it**, and merge on green was
approved for the orchestrating session to perform. Each decision below keeps its authored text as history, with its
ruling stated first; only OD-2's ruling moved delta text.

**OD-1 — CLEARED AS AUTHORED. The packet names.** This is `add-credential-escrow-checkout`; the
successor is `add-credential-escrow-registry`. Brett ruled the SPLIT, not the
names. The pair reads as a sequence and neither collides with an existing change
id. Cost if vetoed: a rename before merge, cheap now and expensive after the
successor cites it.

**OD-2 — VETOED. The schema comes into this packet after all.**

> **RULING, 2026-08-28:** introduce the `escrow:` relationship block on
> `xfactory_credential_binding_template` AND the escrow-entry record kind IN THIS
> PACKET, on ruling A's literal shape. Brett accepted the stated consequence:
> this packet's realization now owes the additive contract cut at the NEXT
> ADDITIVE MINOR, whose number is allocated at realization by merge order and is
> deliberately not spent here. OD-3's deferral of ruling C — the registry home, the
> grandfathered openxpki exception, the three escalation tests — expressly
> STANDS; only the SCHEMA HALF moves here.

**What moved.** A MODIFIED block on "Canonical credential record shapes" (five
kinds become six; two promoted scenarios amended from "five" to "six"; two
scenarios added pinning the additive property), plus ADDED requirements 8 and 9 —
the escrow relationship on the binding, and the entry shape. `code_surface` and
`target_release` were rewritten to declare the schema and the cut, `tasks.md`
§ 4 became a schema realization rather than a fixture pass, and `design.md` § 2
was rewritten as vetoed-and-reversed. Counts went 7 ADDED / 28 scenarios / no
MODIFIED block → 9 ADDED + 1 MODIFIED / 46 scenarios.

**One measured correction the veto surfaced, which strengthens rather than
weakens it.** The cut is owed, but NOT for the usual reason. Parsed here:
`contracts/schemas/xfactory-credential-contracts.schema.yaml` is NOT among the
192 entries of `contracts/releases/contract-v2.0.digests.yaml` — the release
membership closure is built from `contracts/hermes-runtime/contract-index.yaml`
`release_member` entries, and that catalog holds no credential entry. So
release-inventory-drift does not force it. The VERSIONING POLICY does: the schema
is a registered bundle contract (`contracts/manifest.yaml:2079-2094`) and a
registered contract gaining a record kind and an optional field is the additive
minor class verbatim. Stated here so a later reader does not go looking for a
drift finding that will not exist.

**THE AUTHORED TEXT, KEPT AS HISTORY.** ~~This packet carries NO schema surface,
deferring ruling A whole.~~ Brett's ruling A specified the escrow relationship block and the escrow-entry
record kind; ruling D permitted them here "if the checkout path needs them to be
testable". **Measured: it does not.** The checkout path is fully expressible in
the five already-promoted record kinds because the escrow decryption identity is
ITSELF a credential — requirement, binding, grant, audit policy — and the one
field the checkout genuinely needs that the promoted shapes do not name (the
decrypted-object enumeration) is expressible TODAY through
`xfactory_credential_audit_policy.audit.minimum_fields`, which is an open array
of field names. The argument against introducing them anyway: the escrow entry is
half of a RELATIONSHIP, and this packet contains neither the registry the other
half lives in nor the inventory and restore semantics that give the entry its
fields. Landing a half-specified kind would force the successor to MODIFY canon
days old. `design.md` § 2 carries the full argument. Cost if vetoed: the schema
work moves here and the successor loses its reason to exist as a separate packet;
the seven requirements are unaffected either way.

**OD-3 — CLEARED AS AUTHORED, AND EXPRESSLY REAFFIRMED WHEN OD-2 FELL.** Ruling
C is carried to the successor whole, including the grandfathered openxpki
exception. Brett ruled the home and its exception; this packet does not
state them, because the home is a property of the registry. The exception's
disposition is recorded in `tasks.md` as an inherited obligation so it cannot be
lost between packets. Cost if vetoed: one more requirement here, stating a home
for a registry this packet does not define.

**OD-4 — APPROVED AS AUTHORED.** 24 hours to open, 5 business days to dispose,
both bounds from the checkout's end, non-tolling, lateness-is-a-finding. The
policy window's shape and numbers, argued in full above. Brett
ruled that this filing sets a window and asked for a concrete proposal with
reasoning; two bounds, 24 hours and 5 business days, running from the checkout's
END, non-tolling, with waits as `conditions` and lateness as its own finding, are
the authoring session's.

**OD-5 — CLEARED AS AUTHORED. No MODIFIED delta on
`deployment-handoff-boundary`.** Unaffected by the OD-2 veto: the MODIFIED block
that veto forced lands on `credential-contracts`, not on the boundary, whose
promoted text still needs no word changed. Measured against
its promoted text: it already defers to "the governing policy window" and to a
checkout path realized elsewhere. Restating it to add nothing would put a
MODIFIED block on canon for bookkeeping. Cost if vetoed: a MODIFIED block
restating `:51-73` and `:122-135` verbatim with a cross-reference added.

**OD-6 — CLEARED AS AUTHORED. The Flux deploy key ruling is generalized into a
rule.** Brett confirmed
one classification for one credential. This packet states the RE-MINT TEST as a
requirement with the named-retained-authority condition and makes the deploy key
its worked example, because a classification stated for one credential is not
checkable for the next one. Cost if vetoed: requirement 7 drops to a recorded
disposition in `design.md` and the successor inherits the general rule.

**OD-7 — CLEARED AS AUTHORED, and it survives OD-2's fall intact.** The
audit-record enumeration is required through `minimum_fields` rather than through
a new field. As authored, its second reason was that it kept OD-2 true; OD-2 is
now vetoed, so that reason is spent and the FIRST one has to carry it alone — and
it does. The obligation stays inside the promoted `xfactory_credential_audit_policy`
shape, which exists precisely to declare required field names, and the schema
edits this packet now carries are on the BINDING and the ENTRY rather than on the
audit policy. Widening the audit policy too would have been schema work with no
question behind it. **The temptation the veto created and this decision declines:
"the schema is open now, so put the enumeration in it as well."**

## Open Questions — ALL FIVE RULED 2026-08-28

Each was authored with a recommendation and no decision. **Brett ruled FOUR of
the five on this packet's own recommendations and ONE — OQ5 — AGAINST IT**, in
the same multi-choice put over PR #479. Each is shown with its ruling first and
its authored recommendation kept beneath, because a recommendation that was taken
is evidence about the recommendation and deleting it would leave the ruling
looking unsourced — and a recommendation that was OVERRULED is evidence of a
different and more useful kind, which is why OQ5's authored text is kept in full
rather than quietly replaced by the ruling that beat it. No open question
survives this section; the successor inherits obligations, not questions.

**OQ1 — RULED: one drill per client**, on the recommendation. The capability gate
is discharged by one drill; each managed client's first escrow entry then owes its
own per-client-recipient drill before that install is `ready`, and that readiness
obligation is the successor's to state. Recorded as `tasks.md` § 3.6.

_Authored:_ **One drill, or one drill per client?** The gate is "one rehearsed drill".
An operator scope holds many clients, and requirement 5 restricts drills to the
PER-CLIENT recipient, so one drill exercises one client's key.
**Recommendation:** one drill discharges THIS capability's gate and the boundary
milestone; each managed client's first escrow entry then owes its own per-client
drill before that install is `ready` — an obligation that belongs to the
successor's readiness rule, not to this gate.

**OQ2 — RULED: the recommended cadence** — on every escrow-identity rotation,
plus at least annually — set in the successor alongside the rotation runbook,
because rotation is what the cadence is anchored to. Recorded as `tasks.md` § 3.6.

_Authored:_ **Drill cadence after the first.** A path proven once and never again
decays silently. **Recommendation:** on every escrow-identity rotation, plus at
least annually; set in the successor alongside the rotation runbook, because
rotation is what the cadence is anchored to.

**OQ3 — RULED: an explicit scope amendment to `thin-independent-approval`**, on
the recommendation — never a silent reuse. It is a hard precondition of the
drill, recorded as `tasks.md` § 5.4, and its honest effect is to make the drill's
thin approval VISIBLE rather than to fix it.

_Authored:_ **What is "domain approval" at a one-person self-client org?** The
opensoft tenant already carries an accepted-risk record for exactly this shape
(`thin-independent-approval.yaml`: structurally distinct roles, one human).
**Recommendation:** do NOT silently reuse it — its `scope.applies_to` names only
`cir-opensoft-qa-codexfactory-install` and `codexfactory-qa-corebackup`, and an
escrow checkout is neither. Extend it by an explicit scope amendment at
realization, which is also the honest way to surface that the drill's approval
will be thin.

**OQ4 — RULED: the recommended operator-root custody** — the successor's rotation
runbook owns it, and the floor is at least as strong as the per-client key's: an
OFFLINE copy, not a second password-manager item beside the per-client keys,
since a password-manager compromise would otherwise take both halves of the
topology at once. Recorded as `tasks.md` § 3.7.

_Authored:_ **Does the operator root recipient need its own custody ceremony?**
Requirement 5 records its every-client radius but says nothing about how its
private half is held. **Recommendation:** the successor's rotation runbook owns
it, and the floor is at least as strong as the per-client key's — an offline
copy, not a second password-manager item beside the per-client keys, since a
password-manager compromise would otherwise take both halves of the topology at
once.

**OQ5 — RULED: THE DRILL MUST ALSO PROVE A REFUSAL. This is the one ruling that
went AGAINST the authored recommendation, and it is recorded as such rather than
smoothed over.** The drill now has to demonstrate at least one live refusal —
the natural one being a checkout attempted without the recorded human-and-domain
approval — so that the authorization half is proven to BITE and not merely to
have been walked past. Requirement 6's drill definition and `tasks.md` § 5.5 both
carry it. The cost the authored recommendation warned about is real and is
accepted: the boundary milestone now waits on a harder rehearsal.

_Authored:_ **Should the drill be required to fail-closed at least once?** A drill
proves the path works; nothing here proves the path REFUSES. **Recommendation:**
no, not at this gate — the refusals are proven by the negative fixtures in this
packet's code surface, and adding a live refusal to the drill would gate the
boundary milestone on a second, harder rehearsal.

## Impact

- **Capability:** `credential-contracts` — NINE ADDED requirements and ONE
  MODIFIED, 46 scenarios (seven ADDED / 28 / no MODIFIED block as authored, before
  the OD-2 veto). No other capability's spec text moves.
- **Consumed by:** `deployment-handoff-boundary` (its standing-admin exception
  closes on this packet's drill; its policy window is set here).
- **Coordinates with:** `add-trust-anchor` (ACTIVE) — no file in common, and its
  OQ2 promise of no schema change there is kept.
- **Successor:** `add-credential-escrow-registry` — ruling C's home, grandfathered
  exception and three escalation tests (OD-3, reaffirmed at the OD-2 veto);
  inventory completeness and the readiness binding, including OQ1's per-client
  drill obligation; the decryption-free lint that requirement 9's non-secret entry
  makes possible; OQ2's drill cadence; and OQ4's operator-root custody. **Ruling
  A's schema surface is NO LONGER the successor's** — the OD-2 veto moved it
  here.
- **Realizing repositories (successor changes, not this surface):**
  `xFactory-Hermes-Install` (the client credentials tree and the drill record),
  `Omnigent-Install` (the escrow write step in its secret runbook), OpsxFactory
  (the managed-install escrow obligation in its workflow contracts).
- **Staging:** the topic stays staged with exit 1 raised; its `INDEX.md` row and
  detail section are updated in this packet's commit.
