# Identity Brokering Contract Family

Status: ratified
Ratified by: add-identity-brokering (ratified Brett Heap 2026-08-21 — "ratify
both proposals"; realized by Speckit feature `008-identity-brokering-contracts`.
Registered in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at
**contract-v1.37** (2026-08-21), per
[Contract Versioning Policy](../../docs/contract-versioning-policy.md))
Kind: reference
Repository context: openxFactory owns this neutral capability; OpsxFactory owns
the governed `keycloak-administration` workflow, and a new
`xFactory-Keycloak-Install` repository owns the deployable runtime

The neutral contract for **what any identity broker must assert about a human,
what a governed record may store about an actor, and what a broker must never
become**.

Keycloak is the realization the family is adopting. It appears in no schema, no
enumeration and no requirement: what openxFactory owns is the part that
survives the product choice. A domain deploying a different broker, or none at
all, stays conformant and is refused by nothing.

## Why this exists

Three surfaces spent a month converging on the same missing thing.

The openDox workbench is live behind a single shared htpasswd user, so the
answer to "who read this?" is "somebody with the password". The gate console
carries two accepted risks that are both identity shaped — a ratification
record's actor is forgeable, and `--actor` is unauthenticated — which blocks
any write-enabled server-side phase on a proven principal. And the editor
product needs broker logins regardless, with each client insisting on *their*
identity provider.

Cutting across all three: one person works at several companies and several
repository organizations. Identity-per-surface and identity-per-tenant both
fragment that person into unlinkable accounts, which is the outcome to avoid.
One durable persona, with organizations as memberships **on** it.

## The nine rules this family carries

**One persona per human within a broker instance.** The persona is the durable
unit; upstream accounts are contingent — created, retired, renamed and
reassigned by organisations the family does not control — so nothing durable is
built on one. Every federated identity a human uses attaches to their single
persona as a linked identity. No surface holds a human account the broker
cannot resolve to a persona, because an account that resolves nowhere is an
identity the governed layer cannot name.

**Organizations realize company boundaries, on the persona.** The
tenant/operator company and the subject/served company are the same kind of
record — an organization a persona belongs to — never a separate persona and
never a separate identity population. Membership is many-to-many; one persona
may belong to several organizations at once, and leaving a company removes a
membership rather than the persona. An organization may federate its own
upstream provider with domain-routed login. **Membership records association,
not authority.** And a membership NAMES A COMPANY: the membership id admits no
':' and no '/' (so `role:platform-admin` and `stack/<client>/<env>/layer/tenant`
are unrepresentable) and is resolved against the declared organizations in the
same scan, because the one field on a persona assertion that points at another
record was the never-mirror rule's last doorway.

**The broker asserts identity and membership only** — and the property sets are
CLOSED ALLOW-LISTS at every depth, so there is nowhere to put a stack, layer,
domain, project, subject, role, group or grant. A second copy of the tenancy
graph inside an identity product is a copy that will disagree with the first
one, and the disagreement is discovered by an authorization decision going the
wrong way.

**The pointer-not-projection line.** An organization MAY carry exactly ONE
resolvable reference to the governed record it corresponds to, and that
reference resolves in the governed layer. Without it the governed layer cannot
resolve the boundary the broker just named and implementers rebuild the mapping
by string-matching company names — the mirror, arrived at accidentally. With
more than a pointer, broker state becomes a partial copy of the graph. One
reference is legal; copying the referenced record's contents into broker state
is a validation failure, and there is no property in which to copy them.

**Identities link explicitly or merge by decision, never silently.** Two modes
exist and each REQUIRES ITS ACTOR BY SHAPE: a `self_link` initiated by the
human from a session already holding that persona, or an `admin_merge` approved
through the governed administration workflow. Attribute-match auto-linking —
an email address above all — is not representable: an upstream provider may
assert an address it never verified, addresses are reassigned, and the
resulting merge cannot be undone from the audit record. A merge names the
approver, every prior subject identifier, and the time, and every pre-merge
subject stays resolvable to the surviving persona so records already written
against it stay attributable — and the approver is NOT one of the merged
parties. The ratified text says a merge is approved through governed
administration and does not spell that out; the family adopts it as the
faithful reading, because a party approving its own absorption of another
identity is the account takeover the requirement exists to refuse (recorded as
a post-ratification disposition in the feature's research.md).

**A governed record binds its actor to a stable opaque subject.** The settled
shape is the STRUCTURED REFERENCE — issuer (broker instance), opaque subject,
and the display name in force when the record was written. Display names change
and upstream accounts are reassigned; only the opaque subject is durable, and
the denormalized display name is what keeps a record readable without a live
broker. The issuer is what makes a subject interpretable once a second instance
exists, which the isolation rule makes an expected state rather than a
hypothesis.

**History is marked at the boundary, mapped on demand, never backfilled.** A
record written before the broker carries a bare username and says so; it is
never presented as a broker-asserted persona. Where a specific record needs
attribution, an explicitly recorded mapping resolves it and names who mapped
it. A blanket backfill would assert identity resolutions nobody verified.

**Workloads are not personas.** A workload, agent, job or service is not
represented as a persona: its authority comes from `credential-contracts`
grants and `openxwallet` holders, which are strictly stronger than a user row —
attenuated grants, proof of possession, key-attributed audit, revocation that
propagates. A broker service client may be provisioned only where a surface
genuinely needs OIDC tokens, and such a client is TRANSPORT: it holds no
organization membership as authority and never appears as the actor of a
governed act.

**Broker credentials are credential-contract records.** Service-client secrets,
upstream provider client credentials, datastore credentials and administrative
bootstrap credentials alike — each a `credential-contracts` record with
declared custody and a named holder, referenced here and carried nowhere here.
A configuration export used as reviewed state is credential-free BY
CONSTRUCTION rather than by redaction after the fact. Adopting persona login on
a surface running a shared static secret RETIRES that secret, so the inventory
shrinks by the adoption instead of growing. **The claim is always made**: every
adoption declares `prior_shared_credential` as `none` or `replaced`, so the
obligation cannot be satisfied by omitting the field — and the adoption most
likely to leave a shared secret live is exactly the one that never mentions
it.

**Isolation escalates by instance, and the contract is silent on count.** Where
a contract, a regulation or a population's sensitivity forbids co-residence,
the answer is a DEDICATED broker instance with its own deployment, datastore
and administrative plane — never a partition inside a shared one, which pays
the full persona-fragmentation cost for weaker isolation. The silence is
load-bearing in both directions: a single shared instance, a family of
per-client instances, and a single-organization deployment with no operator
layer above it are all conformant. Personas do not span instances, and no
capability may require that they do. **The co-residence answer is recorded
either way**: `restriction_ref` is required for both values — the commitment
that imposes a restriction, or the written finding that there is none. `none` is
the answer a record reaches by default rather than by inquiry, and an unrecorded
negative is indistinguishable from an unasked question.

**A surface declares its authorization posture.** Either access is granted to
any authenticated persona, or it is resolved per action in the governed layer —
and a surface offering a governed WRITE action requires a resolved
authorization decision rather than authentication alone. The failure this
closes is the quiet one: a surface ships read-only under "any authenticated
persona", then gains a write action before per-action authorization exists.
Declaring the posture makes acquiring a write action a visible change of
posture rather than an unremarked commit. NAMING a write action is offering one,
so a populated `actions` list beside `offered: false` is refused by shape — that
combination is the quiet transition already half-made in the record. And because
the decision point is named in free text beside a closed enumeration, the
LOCATOR is checked too: declaring `governed_layer` and then naming the broker's
own administration API is the same substitution one field to the left (see
**Known limits** for what that check cannot reach).

## Custody by composition, not by new vocabulary

This family defines no custody model, no grant, no credential kind and no
authority tier. Every credential it touches is a `credential-contracts` record;
every non-human actor's authority is a `credential-contracts` grant or an
`openxwallet` holder. What the schemas carry is a REFERENCE — the requirement
id, the named holder, and the place custody is declared — so the declaration
lives in exactly one place and the two cannot disagree by restatement.

## The record kinds

| Kind | Purpose |
|---|---|
| `persona_assertion` | The issuing instance, the opaque subject, the display name, the linked upstream identities, the organization memberships. Nothing else, at any depth. |
| `broker_organization` | A company boundary: role (`tenant` \| `served`), routed domains, federated providers by reference, and at most ONE pointer to its governed record. |
| `actor_subject_reference` | What a governed record embeds when it names a human actor: issuer, opaque subject, display name at record, and a provenance discriminator separating a broker-asserted persona from a pre-broker username and from a mapped historical actor. |
| `identity_link_record` | A `self_link` or an `admin_merge`, each requiring its actor by shape, with every pre-merge subject kept resolvable to the survivor. |
| `broker_client_declaration` | A service client declared as TRANSPORT, with the reason OIDC tokens are needed and its credential requirement by reference. |
| `broker_surface_adoption` | The declared posture, the instance and its deployment, the retired shared secret, and the isolation the served population requires. |

## Named consumers

Each pins the released contract bundle rather than copying a shape:

- **OpsxFactory `keycloak-administration`** — the governed administration
  workflow, a sibling of `exchange-administration`,
  `aks-administration-workflow`, `github-administration-workflow` and
  `business-central-administration`, expressed in this vocabulary. It owns the
  merge queue's response time.
- **`xFactory-Keycloak-Install`** — the deployable runtime and its per-client
  `config/clients/<tenant>/runtime-manifest.yaml`, on the hermes-install
  precedent.
- **The workbench oauth2-proxy swap** — the first adoption, retiring the
  htpasswd secret and recording an `authenticated_persona` posture.
- **The gate console `actor_subject` binding** — the gate-action record binds
  its actor to the broker-issued subject plus display name, and because the
  console gains a governed write action it declares `resolved_authorization`.

## What this family deliberately does not do

No broker, realm, organization, deployment, credential, persona or user store.
Contracts, examples and a validator. It changes how no surface authenticates
today, defines no authorization model (memberships are asserted; decisions stay
in the governed layer), obliges no domain to adopt a broker, and mandates no
instance count in either direction.

## Known limits

Every limit this family knows about, in one place. The list is meant to be
complete: a limit a reader has to discover is worse than one they were handed,
and an enforcement scope stated only in a validator comment is not stated.

1. **A declared posture cannot be proven resolved at run time.** The contract
   can check that a posture is declared and that a surface with write actions
   declares the stronger one and names its decision point. It cannot check that
   the resolution HAPPENS. Same honesty limit `openxwallet`'s declared custody
   accepts, and accepted here for the same reason: a declaration a reader can
   audit beats an unstated assumption (design D9).

2. **The credential value scan is a blocklist over the classes it knows.** It
   walks names and values, reassembles adjacent chunks across array items and
   sibling fields, and re-tests each string with its whitespace collapsed — so
   a pasted export, a split export and a spaced-out export are all refused. A
   secret encoded some other way (base64 with no recognizable header, a novel
   assignment syntax, a private key in a format the pattern set does not know)
   passes. Keeping credentials out of free text stays an obligation on
   consumers.

3. **An OPAQUE decision-point ref cannot be adjudicated** (review finding F8).
   `resolved_authorization.resolves_in` is closed to `governed_layer`, and the
   refs beside it are free text. The validator refuses broker-shaped locators
   by shape — broker-administration URI schemes (`keycloak://`, `broker://`),
   broker administration paths (`/admin/realms`, an organization's `/members`
   collection, a realm's user/role/group/client collections), and a scheme-less
   ref whose first segment is the record's own broker instance. It CANNOT
   refuse an internal id, a shortened URL or a team-local name that in fact
   resolves to broker membership. A ref that merely contains the instance id is
   also not refused, deliberately: a governed-layer endpoint legitimately
   scopes itself by instance (`hermes://<instance>/authorization/<surface>`),
   so containment cannot discriminate. This walk catches the honest mistake and
   the lazy shortcut, not a determined one.

4. **Four rules are CORPUS-COUPLED — they resolve only within a single scan**
   (review finding F13). These are rule (b) one-persona-per-instance, rule (i)
   workloads-are-not-personas, rule (l) personas-do-not-span-instances, and
   rule (n) a-membership-names-a-declared-organization. Each resolves a
   reference against the records the scan actually sees, and each is skipped
   rather than failed when the corresponding records are absent.

   **What that means for R6's enforcement scope, stated explicitly:** a
   workload is refused as a persona or as an actor only where the
   `broker_client_declaration` that declares it is in the SAME scan as the
   record that misuses it. Across the D6 repository split — openxFactory owning
   the contracts, a domain repository owning its live records, and possibly a
   third owning the client declarations — the check does not reach. A
   repository that keeps its personas, its organizations and its client
   declarations together gets the full check; one that splits them gets the
   schema and the single-record rules only. Consumers that split them should
   run the validator over a tree containing all three, or accept the weaker
   check knowingly.

5. **An adoption that names no replaced credential is now a claim, not a
   silence** — but the claim cannot be verified. `prior_shared_credential:
   none` is auditable in the sense that a reader can later show it false; the
   validator cannot check it against any credential inventory.

6. **A subject that is a genuinely different string from its display name is
   not caught.** The identifier/display-name comparison runs on the
   alphanumeric skeleton, so removing spaces or punctuation does not defeat it,
   and the `opaque_subject` pattern and length floor carry the short
   substitutions. An abbreviation or an initial-plus-surname in the identifier
   position is a name that no comparison against this record's own display name
   can see (research.md, Decision 5 — the real answer is a broker-issued
   subject FORMAT, which change task 4.4 is positioned to settle).

## Validation

```sh
python3 scripts/validate-identity-brokering.py                 # family self-test
python3 scripts/validate-identity-brokering.py <repo-path>     # repo mode
python3 scripts/validate-identity-brokering.py . --strict       # warnings are errors
```

The self-test runs the packaged corpus under [`examples/`](examples/): every
positive must pass every rule, and every file under
[`examples/negative/`](examples/negative/) must FAIL for the reason declared in
its own first lines. Each negative carries `# expected_failure:`, an optional
`# expected_failure_detail:` pin, and a required `# requirement:` attribution —
and the validator fails if any requirement of the capability has no negative
confirmation, so a requirement cannot quietly lose its probe.

Two vocabularies are READ AT RUN TIME rather than restated: the canonical layer
ids and reserved layer terms come from
[`contracts/policies/layer-vocabulary.yaml`](../policies/layer-vocabulary.yaml),
and the admissible linking bases and authorization resolution point are read
out of these schemas themselves. A check that copied either would be a second
spelling of the thing it enforces.

Coverage closure is PER REQUIREMENT: 14 positives and 41 intended-invalid
negatives covering 9/9 requirements, with a recorded red proof
(`specs/008-identity-brokering-contracts/evidence/`) showing all 22 finding
codes the corpus exercises are load-bearing.

Fourteen of those negatives were added by the adversarial-review hardening of
2026-08-21, one per verified bypass; the findings, their dispositions and the
three that tightened the CONTRACT rather than a check are recorded in
`specs/008-identity-brokering-contracts/traceability.yaml` under
`review_hardening` and in that feature's `research.md`.

Note that the repo-scan layer excludes a packaged or vendored teaching corpus
(`examples/` + `identity-brokering/` in the path) only DURING A DIRECTORY
SWEEP, and reports how many documents it excluded. Naming a file explicitly
validates that file, whatever its path — the one command an author reaches for
when checking a single record used to answer "0 errors" for a file it never
opened.
