---
code_surface: openxFactory — packaged CONFORMANCE FIXTURES ONLY, no schema change. A new `contracts/credentials/examples/` tree carrying the break-glass checkout shape built entirely from the five ALREADY-PROMOTED record kinds (a `xfactory_credential_requirements` record for the escrow decryption identity; a `xfactory_credential_binding_template` recording its approved-secret-provider custody; a `xfactory_runtime_capability_grant_template` for the time-boxed, scope-named checkout; a `xfactory_credential_audit_policy` declaring the decrypted-object enumeration among its `minimum_fields`), plus negative fixtures for the four refusals this packet's requirements name (a runtime decryption-controller recipient reused as an escrow recipient; a checkout grant with no recorded human-and-domain approval; an audit policy omitting the enumeration; a SHOULD-escrow classification naming no retained authority), registered in `contracts/manifest.yaml` and `contracts/CHANGELOG.md` as `type: fixture` members at the next additive bundle cut on the established precedent of the adopted deterministic fixtures at `contracts/manifest.yaml:553-600`. NO change to `contracts/schemas/xfactory-credential-contracts.schema.yaml` — the escrow relationship block and the escrow-entry record kind Brett ruled in A are DEFERRED WHOLE to the successor (OD-2). NO change to any `contracts/trust-anchor/` file, as that change's OQ2 ruling promised. NO validator: the decryption-free escrow lint is the successor's. The Client Hermes realization (the escrow identity's four records under `config/clients/opensoft/credentials/`, the recipient establishment, and the recorded drill) lands in `xFactory-Hermes-Install` and is a successor-repo realization, not this repository's surface.
target_release: next additive contract bundle, allocated AT REALIZATION per `docs/contract-versioning-policy.md` and NOT reserved here. `contract-v2.0` is the declared bundle (`contracts/manifest.yaml:3`), so this lands as `contract-v2.1` at current merge order — stated as an expectation, not a claim, because the `contract-v1.28` renumber sweep is the standing precedent for why a proposal must not spend a minor before merge order is known. THE CLASS IS ADDITIVE: fixtures are added and nothing is narrowed, no schema moves, `contract_schema_version` is unchanged, and every consumer pinned at `contract-v2.0` stays conformant until it upgrades. THE ARCHIVE GATE IS MERGE-PLUS-GREEN PLUS THE DRILL: this packet's realization is not complete on a cut alone, because Brett's ruling D makes ONE REHEARSED DRILL the gate — and that same drill discharges `deployment-handoff-boundary`'s phased-never-gapped milestone.
Status: ratified
Ratified: 2026-08-28 by Brett Heap — four multi-choice selections, each taking the orchestrating session's recommended option, over a read-only decision round on `ideation/staging/client-credential-escrow-registry/`. The four rulings are recorded verbatim in `.openspec.yaml` and restated in § What Brett ruled below. THE CITATION COVERS THE FOUR RULINGS AND THE ADMISSION OF THIS PACKET INTO THE QUEUE, AND NOTHING ELSE. It does NOT cover this packet's requirement text, the proposed policy-window numbers, or the decision to carry no schema surface in this first packet; those are the authoring session's and are flagged for veto in § Orchestrator decisions. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctions for exactly that case, and clears its three-way floor: approver (Brett Heap), date (2026-08-28), and a resolvable record path (this file, § What Brett ruled, and this packet's `.openspec.yaml`).
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
  **This packet carries NONE of it** (OD-2), and § 2 of `design.md` argues why.
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

## The policy window this packet sets

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

This is OD-4: Brett ruled that this filing sets a window; the SHAPE and the
NUMBERS are the authoring session's and are flagged for veto.

## What this changes

Seven ADDED requirements on `credential-contracts`, 28 scenarios, no MODIFIED
block anywhere.

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
   a walkthrough cannot pass for one, and discharging two gates with one act.
7. **The re-mint test decides MUST-escrow from SHOULD-escrow**, with the
   named-retained-authority condition that makes a SHOULD classification
   falsifiable.

## What this deliberately does not change

- **No schema.** `contracts/schemas/xfactory-credential-contracts.schema.yaml` is
  byte-unchanged. Ruling A's `escrow:` block and escrow-entry record kind are the
  successor's, whole (OD-2).
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

## Orchestrator decisions (authored: flagged for veto)

**OD-1 — The packet names.** This is `add-credential-escrow-checkout`; the
successor is `add-credential-escrow-registry`. Brett ruled the SPLIT, not the
names. The pair reads as a sequence and neither collides with an existing change
id. Cost if vetoed: a rename before merge, cheap now and expensive after the
successor cites it.

**OD-2 — This packet carries NO schema surface, deferring ruling A whole.**
Brett's ruling A specified the escrow relationship block and the escrow-entry
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

**OD-3 — Ruling C is carried to the successor whole, including the grandfathered
openxpki exception.** Brett ruled the home and its exception; this packet does not
state them, because the home is a property of the registry. The exception's
disposition is recorded in `tasks.md` as an inherited obligation so it cannot be
lost between packets. Cost if vetoed: one more requirement here, stating a home
for a registry this packet does not define.

**OD-4 — The policy window's shape and numbers.** Argued in full above. Brett
ruled that this filing sets a window and asked for a concrete proposal with
reasoning; two bounds, 24 hours and 5 business days, running from the checkout's
END, non-tolling, with waits as `conditions` and lateness as its own finding, are
the authoring session's.

**OD-5 — No MODIFIED delta on `deployment-handoff-boundary`.** Measured against
its promoted text: it already defers to "the governing policy window" and to a
checkout path realized elsewhere. Restating it to add nothing would put a
MODIFIED block on canon for bookkeeping. Cost if vetoed: a MODIFIED block
restating `:51-73` and `:122-135` verbatim with a cross-reference added.

**OD-6 — The Flux deploy key ruling is generalized into a rule.** Brett confirmed
one classification for one credential. This packet states the RE-MINT TEST as a
requirement with the named-retained-authority condition and makes the deploy key
its worked example, because a classification stated for one credential is not
checkable for the next one. Cost if vetoed: requirement 7 drops to a recorded
disposition in `design.md` and the successor inherits the general rule.

**OD-7 — The audit-record enumeration is required through `minimum_fields`
rather than through a new field.** It keeps the obligation inside the promoted
shape and keeps OD-2 true. Cost if vetoed: a schema change, which is OD-2.

## Open Questions

Each carries a recommendation and no decision.

**OQ1 — One drill, or one drill per client?** The gate is "one rehearsed drill".
An operator scope holds many clients, and requirement 5 restricts drills to the
PER-CLIENT recipient, so one drill exercises one client's key.
**Recommendation:** one drill discharges THIS capability's gate and the boundary
milestone; each managed client's first escrow entry then owes its own per-client
drill before that install is `ready` — an obligation that belongs to the
successor's readiness rule, not to this gate.

**OQ2 — Drill cadence after the first.** A path proven once and never again
decays silently. **Recommendation:** on every escrow-identity rotation, plus at
least annually; set in the successor alongside the rotation runbook, because
rotation is what the cadence is anchored to.

**OQ3 — What is "domain approval" at a one-person self-client org?** The
opensoft tenant already carries an accepted-risk record for exactly this shape
(`thin-independent-approval.yaml`: structurally distinct roles, one human).
**Recommendation:** do NOT silently reuse it — its `scope.applies_to` names only
`cir-opensoft-qa-codexfactory-install` and `codexfactory-qa-corebackup`, and an
escrow checkout is neither. Extend it by an explicit scope amendment at
realization, which is also the honest way to surface that the drill's approval
will be thin.

**OQ4 — Does the operator root recipient need its own custody ceremony?**
Requirement 5 records its every-client radius but says nothing about how its
private half is held. **Recommendation:** the successor's rotation runbook owns
it, and the floor is at least as strong as the per-client key's — an offline
copy, not a second password-manager item beside the per-client keys, since a
password-manager compromise would otherwise take both halves of the topology at
once.

**OQ5 — Should the drill be required to fail-closed at least once?** A drill
proves the path works; nothing here proves the path REFUSES. **Recommendation:**
no, not at this gate — the refusals are proven by the negative fixtures in this
packet's code surface, and adding a live refusal to the drill would gate the
boundary milestone on a second, harder rehearsal.

## Impact

- **Capability:** `credential-contracts` — seven ADDED requirements, 28
  scenarios. No other capability's spec text moves.
- **Consumed by:** `deployment-handoff-boundary` (its standing-admin exception
  closes on this packet's drill; its policy window is set here).
- **Coordinates with:** `add-trust-anchor` (ACTIVE) — no file in common, and its
  OQ2 promise of no schema change there is kept.
- **Successor:** `add-credential-escrow-registry` — ruling A's schema surface,
  ruling C's home and grandfathered exception, inventory completeness, readiness
  binding, and the decryption-free lint.
- **Realizing repositories (successor changes, not this surface):**
  `xFactory-Hermes-Install` (the client credentials tree and the drill record),
  `Omnigent-Install` (the escrow write step in its secret runbook), OpsxFactory
  (the managed-install escrow obligation in its workflow contracts).
- **Staging:** the topic stays staged with exit 1 raised; its `INDEX.md` row and
  detail section are updated in this packet's commit.
