# Design: add-per-tenant-app-manifest-provisioning

Status: draft

The decisions behind ONE `## MODIFIED` block. Each is a fork that was open when
this packet was authored, with the reading NOT taken named beside the one taken.

## D1 — Why the growth goes ON the existing requirement rather than beside it

`credential-contracts`' promoted *Dispatch-only credential least privilege and
serving-tier separation* is a rule about a credential's SCOPE, its BINDING and
what a serving tier may HOLD. Provisioning is a rule about where the credential
CAME FROM. They are different subjects, and a reasonable author would file them
as two requirements.

They are one here, because the provisioning clauses are not independently
motivated: every one of them exists to stop a provisioning path from defeating
the separation clause specifically. "Never by an operator identity" is the
serving-tier sentence read one step upstream — an identity that can mint the pair
IS key material capable of minting a content-write credential. "One pair per
tenant, never shared" is the distinct-binding sentence read across tenants. "The
one named target holds no governed content" is the `actions: write` on the single
repository sentence, made checkable at the moment the repository is chosen rather
than at the moment the token is scoped. Split into their own requirement, each
would read as a new policy with its own justification owed; kept here, each is
the same policy stated where it can still be honoured. RULING `5704187317` (E)
takes the same view by naming a MODIFIED delta and declining the topic's own
offer of a new `install-app-provisioning` capability.

**The cost of the choice, stated.** OpenSpec's MODIFIED REPLACES wholesale, so
this block must carry canon's body paragraph and all three of its scenarios
exactly or silently delete them at promotion. It does — and `doc-health`'s
modified-block-currency family is what checks that claim rather than this
paragraph.

## D2 — The manifest is a SHAPE and the flow is a RUNBOOK, and the line between them

The staged topic carries an operational sequence: ship a manifest, redirect the
tenant, exchange the temporary code, capture app id and private key within the
hour, wire them to the minter. Almost none of that belongs in a neutral contract.

What this delta takes is the part that is FALSIFIABLE FROM A COMMITTED ARTIFACT:
a manifest exists, it is credential-free, it pre-fills NO MORE THAN the scope
the binding may hold — an upper bound rather than an equality, which is what the
requirement sets and what a reviewer can actually refuse against — it names the
tenant-unique identity name, and it names the
one repository the dispatch identity may trigger. Those are readable from the
tree. What it leaves to `Omnigent-Install` is everything only observable at
install time: the redirect, the exchange, the retry, the ordering, which seat
clicks. The test applied was *could a reviewer refuse this from the repository
alone?* — where the answer is no, the sentence went to the installer.

**The one deliberate exception** is the capture window. It is not checkable from
the tree, and it is in the requirement anyway, because the alternative reading is
worse: a provisioning record that does not DECLARE where the material lands is
indistinguishable from one whose author never decided, and the failure mode is a
private key in a pull request. So the clause binds the DECLARATION (the window
and the custody are stated) rather than the act (the material arrives), which is
a shape after all.

## D3 — Case-neutrality, and why the unruled Q2 does not block

The staged topic's Q2 — in the managed `opsxfactory_executed` case does the
operator drive the flow or does the tenant click through? — is one of the two
questions its exit path names as needing a decision. Only Q1 was ruled.

The delta is authored so the answer changes nothing it says. Its clauses bind
WHERE the identity is created (the tenant's own seat), WHOSE it is (the
tenant's), what it MAY REACH (one content-free repository), and what the record
may CARRY (no material). RULING Q3's *"in both cases"* and the topic's own claim
3 (*"the Apps are tenant-owned"* — *"the manifest flow structurally avoids"* an
operator identity in the tenant's credential path) already make all four true in
the managed case and the self-hosted case alike. Q2 decides who CLICKS, which is
a sequence, which is the installer's.

**The reading NOT taken:** waiting for Q2 before authoring. That would have left
a ruled Q1 unexecuted on a question the delta does not ask, and the topic has
already sat from 2026-08-15 to 2026-09-16 past its gate — stated as the two
dates rather than as a day-count, because a count is a figure that goes stale the
day after it is written, which is exactly what happened to the *"exit unraised
twenty days on"* line another topic's fold note carries for this one
(`ideation/staging/INDEX.md:2526-2527`, true when written and not now). What authorizes the authoring is
the ruling's clause (E) directing it, not a finding by this author that Q2 is
dispensable; the topic's gate is not amended here and the topic is not closed
(`proposal.md`, the lifecycle paragraph).

**CASE-NEUTRALITY IS A PROPERTY OF THE WORDING, AND THE FIRST DRAFT DID NOT HAVE
IT.** The clauses as first written said the identity is created "in the tenant's
own organization … and never by an operator identity acting inside it", and that
the captured material lands in "the tenant's own vault". Both are stronger than
case-neutral: canon keeps BOTH operating models legitimate in terms — *"Both
cases SHALL remain legitimate"*
(`openspec/specs/credential-contracts/spec.md:141`) — the ratified runbook
`docs/openxdox-dispatch-credential-binding.md:31-37` records a live
operator-hosted Case A in which the operator creates the App and holds its key
in the OPERATOR's vault, and *An operated identity's credential is held in
governed custody and reached only by reference* puts the custody party in the
BINDING and forbids a contract artifact from naming one. A delta claiming
neutrality while repealing one of the two cases in passing would have been the
worst of both. The clauses now bind the manifest SHAPE and the identity's HOME,
leave the operating model to the per-install execution binding canon already
fixes, and assert the reconciliation in THREE added scenarios — an operator-
executed install driving the flow conforms; the self-hosted individual conforms
from their own account, which is the case canon protects and round 10 found this
block had left without a conforming identity; and a pair already in service that
was created by hand is not retroactively refused.

## D4 — Why the naming convention is a REQUIREMENT clause and not a runbook line

A naming convention reads like style. This one is load-bearing twice, and both
reasons are structural rather than aesthetic. First, the provider's App name is a
GLOBAL slug: two tenants cannot both hold `openXdox`, so a convention is not a
preference but the only way the flow completes for the second tenant. Second, a
per-tenant, pattern-discoverable name is what makes the "never shared" clause
AUDITABLE without reading the tenant's own account — an identity named for one
tenant appearing in another's binding is visible from the binding alone.

The delta therefore states the convention's PROPERTIES (unique per tenant,
discoverable by pattern) and gives the form `<product> — <tenant>` as the shape
rather than pinning `openXdox — <tenant>` as the only lawful spelling: this is a
neutral capability, `openXdox` is one product that consumes it, and the topic's
own Q5 (the grain: display name versus slug) is an installer question the property
survives either way.

## D5 — What this packet refuses to carry, and where each piece went

Three pieces of § 7.4 of `split-opendox-two-layer-product` are NOT here, each on
a recorded disposition rather than an omission.

- **The `openxdox` DNS record.** RULING `5704187317` (B): discharged by NAMING,
  per that packet's own `design.md` § Non-goals (*"beyond naming them"*). The act
  itself is the ceremony-reach widening inside `opensoft/OpsxFactory`'s active
  `add-governed-dns-administration`, owned there on Brett's OQ-E word (issue #207
  comment `5649809425`) and worked by lane opsXfactory-4. It is a five-place
  lockstep, one place of which is a pull request in `opensoft/Opensoft-Tenant`.
- **The `dox` workload set becoming per-tenant.** RULING `5704187317` (D): left
  for the § 3.5 realization. There is one tenant and one plane subject today, so
  a per-tenant declaration would declare a fact that does not exist; and the
  requirement it sits under is under lane opsXfactory-3's claim `5638511222`.
- **The installer.** `Omnigent-Install`'s own change. That repository's README
  puts the boundary in its own words — it *"should not contain … canonical shared
  contracts that belong in `openxFactory/contracts`"* — and CLAUDE.md working
  rule 1 states the same rule from the other side.

## D6 — The per-tenant multiplicity clause, and the bill it implies

`split-opendox-two-layer-product`'s `design.md` § D7 states the cost of RULING Q3
plainly: *"N deployments, N databases, N migration runs per release, N
backup-and-restore policies and N credential sets"*. This delta is the contract
for the last of those five. It says the N credential sets are N, and not one set
used N times — which is the only one of the five that a well-meaning installer
would be TEMPTED to collapse, because the other four are physically impossible to
share by accident and a credential is not.
