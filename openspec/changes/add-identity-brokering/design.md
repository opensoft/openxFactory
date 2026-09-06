# Design: add-identity-brokering

## Context

Organized from the 2026-07-14 brainstorm
`ideation/brainstorm/keycloak-identity-brokering.md` — captured the day the
ideation dashboard shipped behind a single shared htpasswd user and the
question "how do we manage users?" met the gate console's accepted risk
that a ratification record's actor is forgeable — via the staged topic
`openxFactory:staging:identity-brokering-plane`
(`ideation/staging/identity-brokering-plane/`).

That brainstorm named three blockers in its own exit clause: merge safety,
realm topology, and the ownership split. Brett Heap ruled all three in the
xFactory family session on 2026-08-21, and ruled a fourth thing the
brainstorm had not asked about (workloads are not realm users), so the
split was executed the same day. This change is the topic's exit 1: the
neutral contract, and nothing else.

Everything below is a decision already taken, restated with its reasoning
so the reasoning survives the change record. Keycloak appears here as the
adopted realization; it appears in no requirement.

## Decisions

### D1 — A single realm per environment; organizations, not realms

**Decision** (topic R3). The default topology is one realm per
environment, with **Organizations** representing companies — both **tenant**
companies (the operator layer) and **subject/served** companies. Each
organization may federate its own upstream provider with domain-routed
login, so a client's people reach their own provider from a shared entry
point.

**Reasoning.** Realm-per-client was the alternative, and it fragments the
one thing the whole topic exists to protect: a human who works at several
companies becomes several unlinkable accounts. Organizations model
"works at multiple companies" natively — one persona, N memberships,
per-organization provider choice — which is the single-persona argument
against realm-per-tenant rather than a convenience preference.

**In the contract.** Requirements "One persona per human within a broker
instance" and "Organizations realize company boundaries, on the persona".
Neither says "realm" or "Keycloak": the neutral statement is *a single
persona within a broker instance, with organizations realizing company
boundaries*.

### D2 — The broker asserts identity; it never mirrors the governed graph

**Decision** (topic R3). The broker asserts exactly two things: who this
persona is, and which organizations it belongs to. It does not encode
stacks, layers, domains, projects, subjects, roles, or grants.
Authorization resolves in the governed layer, against the Hermes graph and
the grants that already exist there.

**Reasoning.** A second copy of the tenancy graph inside an off-the-shelf
identity product is a copy that will disagree with the first one, and the
disagreement will be discovered by an authorization decision going the
wrong way. One graph, one authority.

**The seam this design adds.** An organization MAY carry a single
resolvable reference to the governed record it corresponds to. Without it,
the governed layer cannot resolve the boundary the broker just named, and
implementers would rebuild the mapping by string-matching company names —
which is the mirror, arrived at accidentally. The requirement therefore
draws the line at *pointer versus projection*: one reference is required
and legal; copying the referenced record's contents into broker state is a
validation failure.

### D3 — Isolation escalates by instance; the contract is silent on count

**Decision** (topic R3). When a client's contract or a population's
sensitivity forbids co-residence, the answer is a **dedicated broker
instance** — its own per-client install — never a second realm inside the
shared broker. The neutral contract stays **silent on instance count**.

**Reasoning, both halves.** Realm-splitting inside one broker buys weaker
isolation than a separate instance (shared administrative plane, shared
database, shared blast radius) while paying the full
persona-fragmentation cost; if we are going to fragment personas we should
at least get real isolation for it. And the silence is load-bearing: a
non-tenanted MedxFactory-style deployment — one clinic, its own stack, no
operator above it — can run its own broker and stay conformant. A contract
mandating one shared broker would make that deployment non-conformant for
no governance benefit.

**In the contract.** "Isolation escalates by instance, never by
fragmenting personas", including the explicit statement that personas do
not span instances and that no capability may require them to.

### D4 — Explicit linking plus an admin-approved merge queue

**Decision** (topic R4). Explicit account linking from a logged-in session,
plus an admin-approved merge queue for pre-existing duplicates. **Never
silent auto-link on attribute match.**

**Reasoning.** Email-match auto-linking is an account-takeover primitive
wherever an upstream provider will assert an unverified or reassignable
address — Entra guest addresses and self-service directories both qualify.
The convenience is real and the failure mode is an identity merge that
cannot be undone from the audit record. A merge is an administrative act
with a record, and it goes through a governed queue like every other
administrative act.

**What this design adds to the ruling.** Two obligations the ruling
implies but does not state: a link or merge record that can name neither an
initiating human nor an approving administrator is invalid (otherwise
"explicit" is unfalsifiable), and pre-merge subject identifiers must stay
resolvable to the surviving persona (otherwise the merge silently
orphans every record already written against the losing identifier —
re-creating, at merge time, exactly the attribution loss the whole
capability is built to prevent).

### D5 — Workloads are not personas

**Decision** (topic R5). Workload identity does not flow through the
broker's user store. It flows through `credential-contracts` (grants
distributed by reference into ephemeral job scope, custody as an execution
binding) and `openxwallet` (grants as the authority primitive, custody
declared and bounding what a signature evidences). Broker service clients
are provisioned only where something genuinely needs an OIDC token.

**Reasoning.** The family already ratified an authority model for non-human
actors and it is strictly stronger than a user row: attenuated grants,
proof of possession, key-attributed audit, revocation that propagates.
Putting workloads in the broker would create a second, weaker authority
vocabulary next to the ratified one — and the weaker one would win by
convenience.

**In the contract.** "Workloads are not personas", with the service client
declared as TRANSPORT: no organization membership as authority, and never
the actor of a governed act. The third scenario refuses the specific
laundering move — a governed record naming a service client as its human
actor — and routes it to `openxwallet`'s unattributed-act rule rather than
inventing a new one.

### D6 — The github-administration ownership split, unchanged

**Decision** (topic R7). openxFactory owns the neutral contract (this
change). OpsxFactory owns the governed administration workflow
(`keycloak-administration`, a **sibling** of the four existing
administration capabilities, not a profile of one of them), with the new
service-subject kind registered in lockstep across `customer-kinds`, the
Hermes template and `stack.yaml`, and grant ceilings in
`credentials/requirements.yaml`. The install repository owns the runtime.

**Reasoning.** The family executed this exact split for GitHub, both exits
archived 2026-07-14/15, and it held. The broker is a managed platform under
the promoted `opsx-service-subject-model` and gets administered the way
every other managed platform is: plan / apply / verify / recover against
reviewed desired state. The lockstep registration matters because those
three files are one registry wearing three filenames — a kind present in
one and absent from another is a validation failure at best and an
ungoverned subject at worst.

### D7 — The install repository is admitted by an ADDED per-repo requirement

**Decision, taken in this change** and a deliberate departure from the
staged topic's exit 3, which proposed a MODIFIED delta to
`repo-boundary-governance`'s "Install repository scope" requirement.

**Reasoning, three independent arguments.**

1. **The ratified template says ADDED.** `repo-boundary-governance` already
   admits a repository this way: "Neutral avatar-client repository
   boundary" is a per-repo requirement naming its creating successor
   change, its ownership, its explicit MUST NOTs, and — separately —
   "Deferred aggregation and web-console integration" for admission. The
   newest precedent in the capability is one requirement per repository,
   not a growing enumeration.
2. **A MODIFIED delta would collide with the sibling.** A MODIFIED
   requirement wholesale-replaces the named requirement. `add-trust-anchor`
   admits `openxpki-install` from the same session; if both changes issued
   MODIFIED deltas against "Install repository scope", whichever archived
   second would silently drop the first one's admission. Two ADDED
   requirements with distinct names cannot collide.
3. **The enumeration is not the right home anyway.** "Install repository
   scope" says what install repositories are *scoped to* (install,
   operations, backup, restore, upgrade, verification, DR). It carries no
   per-repo ownership, no creating change, no contract pin, and no
   prohibitions — all of which the broker repository needs. Widening a
   scope sentence would admit the repo without governing it.

**Consequence to accept.** `Hermes-Install` and `Omnigent-Install` remain
enumerated in the older requirement while the newer repositories are
governed per-repo. That inconsistency is real and is worth a later
consolidation change; it is not worth coupling this change to a rewrite of
a ratified requirement it does not otherwise touch.

### D8 — Credential custody by composition, not by new vocabulary

**Decision** (topic composition section). Broker datastore credentials,
upstream provider client secrets, and confidential-client secrets are all
`credential-contracts` records with declared custody. Nothing is
committed. Retiring the dashboard's htpasswd secret **removes** today's one
shared secret rather than adding to the inventory.

**Reasoning.** This needed no ruling — it is what composition means. The
requirement exists anyway for two reasons the composition alone does not
cover: a configuration or realm export is the specific artifact that
smuggles credentials into a repository while looking like desired state,
and the retire-the-old-secret obligation is what keeps an adoption from
leaving two authentication paths live.

### D9 — A declared authorization posture

**Decision, taken in this change**, as the half of open question OQ-2 that
does not require settling v1 scope.

**Reasoning.** OQ-2 (login-only versus authorization gating at v1) is
carried, not resolved. But the topic names its own risk precisely: a
surface ships read-only, then gains a write action before the
authorization delta lands. That risk can be closed without answering OQ-2
— require the posture to be declared, and require a governed write action
to have a resolved authorization decision. Whichever way OQ-2 goes, the
silent transition from read-only login to write-enabled login stops being
possible.

### Post-ratification note, 2026-09-05 — the install-repo rename (#242) and the origin declaration

The origin declaration in `.openspec.yaml` names
`xFactory-Keycloak-Install`, and that is the name it will keep. It is the
name Brett Heap's 2026-08-21 rulings were recorded under at the ratifying
commit `1570ff7e`, and an origin declaration is the record of why this
change was created — not a description of the world as it stands today.

**What was renamed.** Later the same day, Brett Heap ruled the broker and
CA install repositories Opensoft-level operator infrastructure rather than
xFactory-product repositories, and the sweep in commit `e11a057b` (PR #242,
"Amend install-repo naming to Opensoft-level: Keycloak-Install +
OpenXPKI-Install") renamed them unprefixed on the CloudPC-Install /
Omnigent-Install precedent. The names that hold from that ruling forward:

- `opensoft/Keycloak-Install` (was `opensoft/xFactory-Keycloak-Install`),
  aggregation path `installs/keycloak-install`, admitted by the ADDED
  `repo-boundary-governance` requirement this change carries and created by
  the successor `implement-keycloak-install-repo`.
- `opensoft/OpenXPKI-Install` (was `opensoft/xFactory-OpenXPKI-Install`),
  the sibling `add-trust-anchor` admits.

Aggregation paths and successor change ids were unchanged by the rename;
the amendment is recorded in this packet's `proposal.md` closing paragraph,
and D6 / D7 above are unaffected — the split and the per-repo admission are
what they were, under a different repository name.

**What that sweep also touched, and why it is being undone.** `e11a057b`
applied the rename to the origin declaration as well. Its one hunk there
was:

```text
-    `xFactory-Keycloak-Install` runtime (exit 3) are named successors that
+    `Keycloak-Install` runtime (exit 3) are named successors that
```

so `origin.reason` came to read "the `Keycloak-Install` runtime (exit 3)
are named successors that consume this contract's vocabulary, which is why
it ratifies first". That edit is a post-ratification mutation of a ratified
origin declaration, which `release-realization` § "Origin retention at
archive" forbids and the gate landed by #695 refuses. The declaration has
been restored byte-for-byte to its bytes at `1570ff7e`; the sentence above
is where the renamed name now lives, so nothing the sweep said is lost. The
disposition for the restoration is Brett Heap's ruling of 2026-09-05,
"restore all four, land them when green" (issue #709).

This is the same treatment the rest of the packet's historical material
already gets: `supporting-docs/source-snapshots/identity-brokering-plane.md`
and `review/co-residence-finding-2026-08-21.md` both keep the pre-amendment
name as provenance, and `e11a057b` left them alone for that reason. The
origin block belongs in that set and is now back in it.

**The operational rule, going forward.** A corpus-wide sweep MUST NOT touch
a ratified packet's origin block: the sweep's own subject matter — current
names, current paths — is exactly what an origin declaration is not about.

## Open questions carried forward

Each has a recommendation. None is settled by this change; OQ-5 is a gate
on ratification rather than an item to resolve at realization.

### OQ-1 — The durable subject in governed records

Store the broker's opaque subject identifier with a denormalized display
name? And what happens to records written before the broker existed, which
carry bare usernames — a mapping table, a one-time backfill, or leave
history as-is and mark the boundary date?

**Recommendation.** Opaque subject plus denormalized display name, yes:
the display name keeps a record readable without a live broker, and the
opaque subject is the only durable identifier. For history: **mark the
boundary date and add mapping entries only where a specific record needs
attribution**. A blanket backfill asserts identity resolutions nobody
verified — precisely the false-audit failure the merge ruling refuses — and
a mapping table that must be complete before the broker is useful would
stall the whole adoption. The requirement already forbids presenting a
bare username as a broker-asserted persona, which is the property that
must hold either way.

### OQ-2 — Login-only versus authorization gating at v1

**Recommendation.** Login-only first (any persona in an organization may
read), with authorization as its own later delta consuming organization
memberships plus the project register — and D9's declared posture as the
guard rail, so the named risk is closed without pre-committing the
authorization design.

### OQ-3 — The exact `actor_subject` field shape

Single opaque identifier, or a small structured object (issuer + subject +
display name)?

**Recommendation.** The structured reference. It is more honest across a
future broker migration or a second broker instance, where a bare subject
is ambiguous without knowing who issued it — and D3 makes multiple
instances an expected state, not a hypothetical. The cost is a wider field;
the cost of guessing the other way is a schema major. The requirement
deliberately fixes what must hold and names the shape as open, so the
consuming change (the gate-console binding) settles it against a real
record.

### OQ-4 — `hermes-readiness` bearer-token adoption

**Recommendation.** Not in the first wave. The readiness surface is a
worker-facing, non-human path, and its auth modes are being settled by the
worker-enrollment broker's own work; moving it to broker-issued tokens now
would couple this adoption to that unsettled design for no persona-side
benefit. Revisit once enrollment auth modes land — and note that under D5
the readiness surface's caller is a workload, so its eventual answer is
more likely a grant than a persona token.

### OQ-5 — Co-residence check (PRE-RATIFICATION GATE)

**This is a gate, not an item.** Before ratification, verify whether any
current commitment implies a user population that must **not** co-reside in
the shared realm. The two candidates named by the topic are the Medx
clinical surfaces and the Business Central / DaVinciSite tenant work.

**Why it gates.** D3 says isolation escalates by instance. If such a
population already exists, it becomes the first dedicated-instance client
and the contract's silence on instance count is exercised immediately
rather than theoretically — which is evidence the requirement is right. If
one exists and is missed, the first adoption puts a population into a
shared instance that a commitment forbade, and the remedy after the fact is
a migration rather than a deployment choice.

**Recommendation.** Answer it as a written finding before ratification,
naming each candidate population and the commitment consulted, even when
the answer is "none found" — an unrecorded negative is indistinguishable
from an unasked question.

## What this deliberately does not do

- No broker, no realm, no organization, no deployment, no credential, and
  no user store. Contracts, examples, and a validator.
- No change to how any surface authenticates today. The htpasswd
  dashboard keeps working until the oauth2-proxy successor lands.
- No modification to any existing requirement, in
  `repo-boundary-governance` or anywhere else. The one existing capability
  touched gains a requirement and loses nothing.
- No authorization model. Memberships are asserted; decisions stay in the
  governed layer, and the per-action authorization delta is a named
  successor.
- No obligation on any domain to adopt a broker, and no instance-count
  mandate in either direction.

## Risks

**The mapping seam becomes the mirror.** D2 permits one pointer from an
organization to its governed record. The failure mode is incremental: a
second field for convenience, then a third, until broker state is a
partial copy of the tenancy graph that disagrees with it. The validator
must enforce the persona-assertion and organization property sets as a
CLOSED ALLOW-LIST rather than a denylist of forbidden names, because a
denylist admits every field nobody thought to forbid.

**The declared posture is a declaration.** D9 can be satisfied by writing
`resolved_authorization` and resolving nothing. A validator can check that
a posture is declared and that a surface with write actions declares the
stronger one; it cannot check that the resolution happens. That is the same
honesty limit `openxwallet`'s declared custody accepts, and it is accepted
here for the same reason: a declaration a reader can audit beats an
unstated assumption.

**Merge safety versus adoption friction.** An admin-approved merge queue
with no administrator watching it is a queue of humans locked out of their
own personas. The administration workflow (D6) owns the response time, and
the risk belongs on its side of the split — but it belongs to this
decision, because D4 is what creates the queue.

**One persona as a single point of compromise.** Consolidating a human
into one persona concentrates the consequence of that persona being taken
over — the counterweight to the fragmentation argument. The mitigations are
not in this contract (upstream provider strength, step-up authentication,
session policy); what this contract can do, and does, is refuse the silent
auto-link that would make takeover easy, and keep authorization resolving
in the governed layer so a compromised persona still has only the grants
the governed graph gives it.
