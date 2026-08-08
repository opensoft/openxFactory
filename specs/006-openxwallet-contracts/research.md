# Research: openxWallet neutral contracts

**Feature**: `006-openxwallet-contracts`
**Governing change**: `add-openxwallet` (ratified 2026-08-07, Brett Heap)

This file records the two decisions the ratified change left to this feature,
both of which the handoff flagged as more than routine work, plus the
convention and dependency findings the implementation rests on.

## Decision 1 — the closed custody enumeration (change tasks.md 2.2)

### What the ratified text constrains

> a key readable by the holder's own execution context evidences that the
> ENVIRONMENT acted, and only custody isolating the key from that context
> evidences that the HOLDER acted. These SHALL NOT be presented as equivalent.

That is two logical facts, not one:

- `readable → evidences = environment`
- `evidences = holder → isolated` (the force of "only")

The second is a NECESSARY condition, not a sufficient one. Isolation is
required for a holder claim; the ratified text does not say isolation alone
earns it. Reading it that way is what lets the set carry a third member
without contradicting the ruling, and the reading is recorded here because it
is the one interpretive call this feature makes.

### The failure mode being defended against

A two-member set (`readable` / `isolated`) satisfies the letter of the ruling
and re-opens the hole one level down. It lumps a local signing daemon the
holder's process can call without limit together with a key requiring a
per-signature authorization that process cannot supply. Under a two-member
set the daemon claims the hardware key's authority — the same collapse the
ruling closes, moved down a level.

The discriminator that actually separates them is not where the key lives. It
is whether the holder's own execution context can obtain a signature at will.
If it can, a compromised environment signs anything the holder could, and the
signature cannot distinguish "the holder decided" from "something running as
the holder decided".

### The set — three members, two declared booleans, derived `evidences`

| id | key readable by holder's execution context | per-use authorization outside that context | evidences | ceiling |
|---|---|---|---|---|
| `holder_readable` | yes | no | `environment` | `act` |
| `isolated_invocable` | no | no | `environment` | `act` |
| `isolated_per_use_authorized` | no | yes | `holder` | `act_unsupervised` |

`evidences` is DERIVED, never independently asserted:

```
evidences = holder   iff   (not readable) and per_use_authorization
           environment otherwise
```

The validator enforces the derivation, and enforces two further invariants:

- **`custody-ceiling-unearned`** — a ceiling of `act_unsupervised` requires
  `evidences: holder`.
- **`custody-collapse`** — every member readable by the holder's execution
  context must sit strictly below every member evidencing the holder. This is
  the handoff's failure mode stated directly as a check: the readable case
  cannot reach the isolated case's authority.

Together these make the collapse structurally impossible rather than merely
discouraged. The handoff's warning was that a collapsed enumeration "would
all validate cleanly"; under these three checks it does not validate at all.

### Why the ceilings sit where they do

`holder_readable` reaches `act` rather than stopping at `request`. Capping
software custody below `act` would stall the first consumer — LedgerxFactory's
posting agent must COMPLETE a post, and there is no key infrastructure in the
stack today. That is precisely the outcome the ruling rejected when it
declined to mandate hardware backing. Approval-before-apply is the
compensating control: a distinct authority reviews, so environment-level
evidence is survivable. Only `act_unsupervised` — an irreversible effect with
no approval before apply — requires evidence that the HOLDER acted.

`holder_readable` and `isolated_invocable` share a ceiling and differ in
nothing the ceiling can express, which is honest: isolation without per-use
authorization buys containment of the KEY (it cannot be exfiltrated and
replayed off-platform) rather than attribution of the ACT. The distinction
still does real work, because the audit requirement demands a reader can tell
whether the holder or its environment was evidenced, and the record carries
the declared booleans either way.

### The authority ladder

Ordered, ascending, closed. Each tier is defined by what the holder can do
ALONE:

1. `attest` — record assertions; no external effect.
2. `request` — initiate an act a DISTINCT holder must complete or approve.
3. `act` — complete an effecting act; approval before apply required.
4. `act_unsupervised` — complete an effecting act with no approval before
   apply.

Approving is not a tier; it is an effecting act, expressed as scope, and
`authority_agents_may_approve: true` therefore requires tier ≥ `act`.

### Deliberate non-members

- **No asserted or keyless custody.** The core requires proof of possession.
  A member for "identity asserted, not proved" would re-open the hole the
  capability exists to close. The staged fragment's open question 2
  recommended exactly this; any interim belongs in the consuming domain as a
  recorded, dated exception rather than as a softening of the neutral set.
- **No shared-credential custody.** A shared key destroys attribution, and
  the key-attribution requirement already rules the case: an act attributable
  only to a shared credential is recorded as `unattributed`, never assigned
  to a holder. A custody member for it would contradict that requirement.

## Decision 2 — what the composition component set covers (change tasks.md 3.2)

### The tension

Include a fast-changing retrieval corpus and revocation fires constantly and
gets routed around. Exclude it and an agent's behaviour changes without its
identity changing. The profile requires the set to be DECLARED, which makes
the choice visible but does not make it.

### The resolution: declare a binding mode per component

The include/exclude framing is a false binary. It treats "the corpus" as one
thing when it is two: the corpus's GOVERNING CONFIGURATION (which corpus,
what may be retrieved from it, under what selection rules) and the corpus's
CONTENTS (the documents in it right now).

Every declared component carries a `binding_mode`:

- **`content`** — the component's own digest enters the composition hash.
  Changing the component changes the hash and revokes. Used for model
  version, prompt contract, tool manifest, policy version, parameters.
- **`reference`** — the component's IDENTITY and GOVERNING CONFIGURATION
  enter the hash; its row-level contents do not. Used for retrieval corpora.

So for a retrieval corpus the hash covers WHICH corpus, WHAT the agent may
retrieve from it, and UNDER WHAT rules it is consulted. Swapping the corpus,
widening the retrieval scope, or changing the selection or admission
configuration all change identity and revoke. Documents arriving in an
already-governed corpus do not, because the agent's authority has not
changed — the corpus has its own governance, and borrowing this mechanism to
police it would be the wrong control in the wrong place.

### Why this is not "exclude the corpus with extra words"

The excluded thing is narrow and named: row-level contents of a corpus whose
identity and governing configuration ARE covered. An agent cannot change what
it may retrieve, or from where, without changing its identity. That is the
behaviour-change case the exclusion was feared to admit, and it is covered.

### Why it satisfies the profile's actual requirement

The requirement is that a reader can tell what a matching hash was asserting.
`binding_mode` per component is what makes that legible: the record states
not just WHICH components are covered but HOW each is covered. A hash whose
corpus is bound by reference asserts something strictly weaker than one
binding it by content, and the record says so rather than leaving a reader to
assume.

Both binding modes remain available for every component, so a domain that
wants content binding on a slow-moving corpus may declare it. The contract
makes the choice visible and checkable without making it for anyone.

## Dependency finding — `approval_policy` is an object, not a flat enum

`contracts/schemas/hermes-job-envelope.schema.yaml` defines `approval_policy`
as an object with three required properties:

- `hermes_approval_required_before_apply` (boolean)
- `authority_agents_may_approve` (boolean)
- `human_escalation_required_for` (array of string)

The profile requirement — "SHALL admit the neutral job envelope's
`approval_policy` values as legal scope terms" — therefore means a grant's
approval posture draws its KEYS from that property set. The tenth negative
confirmation, "an authority term outside `approval_policy`", is a key outside
that set.

**The validator reads the legal vocabulary out of the canonical envelope
schema at runtime rather than restating it.** That is the whole point of the
requirement — one vocabulary rather than two that must be kept in agreement —
and hardcoding the three names here would recreate the second vocabulary the
requirement forbids.

Posture and tier are bound to each other so the two cannot disagree:

- `hermes_approval_required_before_apply: false` requires tier
  `act_unsupervised`.
- `authority_agents_may_approve: true` requires tier ≥ `act`.

## Convention findings

- **Family layout** follows the `contracts/worker-enrollment/` shape:
  `contracts/openxwallet/` holding `*.schema.yaml`, a `README.md` carrying a
  `Status:` header, and `examples/` with `examples/negative/`.
- **Schemas** are JSON Schema Draft 2020-12 written in YAML, each carrying
  `schema_version: 1`, a `kind:`/`name:` line, `$schema`, an absolute `$id`
  under `https://xforge.us/schemas/openxfactory/openxwallet/v1/`,
  `contract_id`, and `contract_schema_version: 1`.
- **The validator** is standalone (no shared helper module), resolves its
  root as `Path(__file__).resolve().parents[1]`, collects findings through a
  `Findings` class emitting `ERROR [kebab-code] message`, runs a self-test
  layer over the packaged corpus plus an optional repo-scan layer, and exits
  0 clean / 1 findings / 2 harness error.
- **Negative fixtures** use the dominant repo dialect: a first-line
  `# expected_failure: <code>` header with an optional
  `# expected_failure_detail: <substring>` pin. The detail pin matters here
  because several of the ten cases would otherwise collapse into a generic
  `schema` finding and stop testing the invariant they are named for.
- **Coverage closure** is added on top of the dialect: each negative also
  declares `# requirement: <REQ-ID>`, and the validator fails when a
  requirement in the closed list has no probe, when a registered probe has no
  file, or when a file carries a requirement id that is not in the list. That
  is what makes the corpus a negative confirmation PER REQUIREMENT rather
  than a pile of negatives.

## Correction to the handoff's origin-checker caution

The handoff states that a `Staging ID:` header wrapped in backticks does not
match and reports the linkage as broken. That described the original regex;
it was loosened in commit `b999f79` to
`^Staging ID:\s*`?([^`\s]+)`?\s*$`, which tolerates backticks. What breaks it
now is any prefix before the header — a Markdown bullet (`- Staging ID:`) or
bold (`**Staging ID**:`) fails the `^` anchor under `re.M`.

The linkage for this change is currently intact and is left untouched: the
topic document carries the plain, column-0 form at line 18. The habit the
handoff recommends is still the right one.
