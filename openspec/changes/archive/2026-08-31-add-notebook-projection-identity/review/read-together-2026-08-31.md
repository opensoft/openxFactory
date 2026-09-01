# The three packets read together: `credential-contracts` after the inverted archive order

Status: record
Date: 2026-08-31
Verifier: Claude Opus 5 (agent), read-only measurement in an isolated scratchpad
clone branched from `origin/main` `4290cad2`; nothing in the three archived
packets was edited.

## What this record is, and what it discharges

This is the READ-TOGETHER that three archived packets left owed and that
**opensoft/openxFactory#545** filed as a successor act. It reads the promoted
`credential-contracts` text — and the `lifecycle-notebook-projection` text where
the same three packets landed deltas — as it now stands in canon, and asks
whether the three sets of deltas COMPOSE.

It discharges the SUBSTANCE of two boxes that cannot themselves be ticked:

| box | where it lives | what it asked |
| --- | --- | --- |
| § 6.2 | `openspec/changes/archive/2026-08-31-add-notebook-hosting-credential-custody/tasks.md` | *"the two changes' `credential-contracts` text should be read together once both are promoted"* |
| § 7.3 | `openspec/changes/archive/2026-08-31-add-binding-consumer-identity/tasks.md` | the mirror of the same, *"whoever archives `add-notebook-projection-identity` discharges both"* |

**BOTH BOXES REMAIN UNTICKED AND THIS RECORD DOES NOT TICK THEM.** They sit
inside archived records, which this estate's doctrine forbids amending — the same
doctrine `add-notebook-projection-identity`'s own § 8 invoked when it declined to
reach into those two packets. What was owed was a READING ACT WITH FINDINGS OF
ITS OWN, and this file is that act's evidence. The unticked boxes are the honest
state of two closed records; this record is the discharge.

## The inverted order, in one paragraph

The ruled chain order was B → C → D: `add-notebook-projection-identity` (B),
then `add-notebook-hosting-credential-custody` (C), then
`add-binding-consumer-identity` (D). It did not run that way. **PR #538**
(squash `3a6a16e9`) swept the four standing MODIFIED-over-a-sibling's-ADDED pairs,
wrote D's `Modified over` marker and struck C's falsified fifth scenario. **PR
#541** (merge `2f1cd139`, archive commits `d02ef5a5` then `b09e59da`) then archived
C and D basis-first, on Brett Heap's Route-1 ruling of 2026-08-31 — while B was
still in its review rounds. **PR #539** (squash `4290cad2`) landed B last. Both of
C's and D's archived copies restate their reconciliation box, dated 2026-08-31,
as *"the obligation attaches to THAT change's archive … whoever archives
`add-notebook-projection-identity` discharges both"*; B's § 8 answers in terms
that its archive does NOT perform the reconciliation, supplying only the
precondition — the operated-identity generalization becoming canon — and naming a
successor act. **Issue #545** is that successor's filing, and this record is its
evidence.

## Method

Measured against `origin/main` `4290cad2` in a fresh clone. Each of the twelve
promoted requirement blocks the three packets touch was extracted from
`openspec/specs/<capability>/spec.md` and compared, whitespace-trailing-normalized
only, against the block in its own archived delta. Scenario bodies were compared
individually by `sha256`. Counts were taken with `grep -c '^### Requirement'` and
`grep -c '^#### Scenario'` on the promoted spec file AT EACH COMMIT of the archive
chain, so the arithmetic of the composition is read rather than asserted.

### The chain, measured at each landing

| commit | act | `credential-contracts` | `lifecycle-notebook-projection` |
| --- | --- | --- | --- |
| `881e1c05` | the tip before the three | 7 reqs / 24 scen | 14 reqs / 52 scen |
| `d02ef5a5` | C archives (#541) | 9 / 33 | 15 / 56 |
| `b09e59da` | D archives (#541) | 12 / 64 | 15 / 56 |
| `4290cad2` | B archives (#539) | 12 / 67 | 18 / 74 |

C contributes **3 requirements / 13 scenarios** (2 reqs + 9 scen to
`credential-contracts`, 1 req + 4 scen to `lifecycle-notebook-projection`).
D contributes **3 added requirements / 30 scenarios plus one scenario onto the
requirement it MODIFIES** (+31). B contributes **3 scenarios onto the
`credential-contracts` requirement it MODIFIES**, and to
`lifecycle-notebook-projection` **3 added requirements / 17 scenarios plus one
scenario onto a MODIFIED requirement** (+18).

### The twelve blocks, and how each stands

| capability | requirement (promoted line) | provenance | delta → canon |
| --- | --- | --- | --- |
| `credential-contracts` | The credential vault operator is an execution binding, never contract content (L133) | B MODIFIED | byte-identical, 5 → 5 scen |
| `credential-contracts` | An operated identity's credential is held in governed custody and reached only by reference (L210) | C ADDED | byte-identical, 4 → 4 scen |
| `credential-contracts` | Each consuming system reaches a shared operated identity through its own binding (L237) | C ADDED, then D MODIFIED | canon carries **D's** block byte-identical, 6 → 6 scen; C's earlier text is superseded, by design |
| `credential-contracts` | A credential binding declares the consuming system that holds it and the identity it fetches with (L278) | D ADDED | byte-identical, 12 → 12 scen |
| `credential-contracts` | Two bindings on one secret are refused unless every pair declares distinct consumers … (L440) | D ADDED | byte-identical, 12 → 12 scen |
| `credential-contracts` | A declared consumer makes access revocation readable and does not make a bearer secret unshared (L577) | D ADDED | byte-identical, 6 → 6 scen |
| `lifecycle-notebook-projection` | Projection implementation ownership (L145) | B MODIFIED | byte-identical, 3 → 3 scen |
| `lifecycle-notebook-projection` | The session namespace is reconciled against live sessions (L348) | B MODIFIED | byte-identical, 7 → 7 scen |
| `lifecycle-notebook-projection` | The hosting record declares where the hosting identity's credential is held, by reference only (L420) | C ADDED | byte-identical, 4 → 4 scen |
| `lifecycle-notebook-projection` | The projection's hosting identity is declared at install (L447) | B ADDED | byte-identical, 5 → 5 scen |
| `lifecycle-notebook-projection` | Access to the projection is shared out from the hosting account, and each share act is recorded (L478) | B ADDED | byte-identical, 5 → 5 scen |
| `lifecycle-notebook-projection` | A hosting-account migration re-derives, proves parity, then retires the originals by recorded act (L519) | B ADDED | byte-identical, 7 → 7 scen |

**Eleven of twelve blocks stand byte-identical with their archived deltas. The
twelfth is the one title two packets write, and canon carries the later of the
two whole** — which is what a MODIFIED-over-a-sibling's-ADDED pair promoting in
the safe order is supposed to look like.

## (a) C's thirteen promoted scenarios stand, with the struck fifth absent

**HOLDS.** All 13 are in canon.

- 4 scenarios of `credential-contracts` L210, byte-identical.
- 4 scenarios of `lifecycle-notebook-projection` L420, byte-identical.
- 5 scenarios of `credential-contracts` L237 — the requirement D restates —
  carried inside D's block and each byte-identical with C's delta: *A second
  system needs the same identity* (`sha256` `2fa930cb…`), *One system's access is
  revoked* (`9689d2d6…`), *A consumer that already holds the secret must be
  evicted* (`cff5151d…`), *The access log is asked which system read the secret*
  (canon L265–267, `md5` `89797f38…` equal to the delta's L56–58), *A shared
  session is proposed instead of a second binding* (`e1bdad56…`).

The struck fifth — **"The published binding shape cannot yet express the access
identity"** — is ABSENT from canon: `grep -rn` over `openspec/specs/` returns
**0**. Repository-wide, the title survives in exactly two places, both correct as
history: C's own archived delta, where the dated `**AMENDED 2026-08-31**` note at
`specs/credential-contracts/spec.md:60-89` records the strike, its authority
(Brett Heap, the ratifying owner) and its ground (the falsified-scenario clause
of `govern-sibling-added-modified-deltas`); and D's `design.md:641`, which quotes
the title precisely in order to say it *"is FALSE"*. **No promoted text and no
live document asserts the struck claim.**

## (b) D's requirement is five carried scenarios plus one addition

**HOLDS, AND IS A PURE ADDITION.** Canon L237 carries six scenarios: the five
above, byte-identical, in C's own order, plus one inserted before *A shared
session…* — **"The binding shape expresses the consuming system and its fetch
identity"** (canon L269–272; `sha256` `2354a7d7…`), whose body is
the `consumer:` framing: *"each names the consuming system that holds it and the
identity it fetches with, so the per-system authority is READ from the record
rather than asserted"*, bounded by *"reconciling that declaration against the
store's actual grants remains a live-estate act this shape does not perform."*
**Zero units lost, zero units substituted.** D's § 7.4 asserted exactly this
after #538's strike; measured here against CANON rather than against the
sibling's delta, the assertion is TRUE.

D's block also adds three prose paragraphs C did not have, none of which
displaces a C paragraph: the record-fact paragraph (*"THE AUTHORITY IS A RECORD
FACT, NOT AN ASSERTION ABOUT THE ESTATE"*, with its own guard that the
"describes a pair as proven" obligation is the requirement's and not a
checker's); a sentence appended to C's honest-reach paragraph — *"Declaring the
consuming system and its fetch identity SHALL NOT be read as narrowing that
limit: it makes the revocable thing nameable, not the disclosed thing
recallable"*; and the `Modified over` marker (canon L248). The appended sentence
is the reconciliation the composition needed: it stops D's readability gain from
being read as the containment C explicitly refused to claim.

## (c) B's operated-identity generalization reads coherently with both

**HOLDS — AND IT CLOSED A REFERENCE THAT WAS DANGLING IN CANON.**

C's promoted requirement opens (canon `credential-contracts:211`): *"The existing
prohibition on hard-coding an operated identity's credential states what must not
happen; this states what must."* **That prohibition is B's, and B landed last.**
Measured at `b09e59da` — C and D promoted, B not yet — the vault-operator
requirement in canon contained NO occurrence of `OPERATED IDENTITY`, and its only
hard-coding prohibition read *"a vault operator, a vault product, or any secret
value"*. **C's presuming clause pointed at nothing in canon for the span of two
commits, both landed 2026-08-31.** `4290cad2` supplies the antecedent at
`credential-contracts:137`: *"The same rule SHALL govern any OPERATED IDENTITY the
family stands up … Contract artifacts SHALL NOT hard-code the identity itself, its
operator, or any credential for it. Custody is the general rule; the vault is its
first instance."* The reference now resolves, and the sentence C wrote is the
sentence B's paragraph answers.

Three further seams were read and hold:

- **The two-case model is stated identically in all three.** B's
  `credential-contracts` block: *"Self-hosted operation … SHALL carry no
  obligation to stand up an organizational identity it has no operator for."*
  C's `lifecycle-notebook-projection` block: *"A SELF-HOSTED declaration SHALL NOT
  be required to name custody."* B's `lifecycle-notebook-projection` block:
  *"Both cases are legitimate; the second is not a degraded form of the first."*
  C's *"an operated identity with no declared custody is not governed"* does not
  contradict the carve-out: C scopes itself to identities **the family stands
  up**, and a self-hosted installer's own account is not one.
- **The personal-identity refusal composes as general-to-instance.** B's
  `credential-contracts` block refuses *"a personal identity merely designated as
  the organization's"*; B's `lifecycle-notebook-projection` block refuses *"a
  consumer account merely designated as the company's"* on the named grounds
  (no administrative console, no enforceable organizational policy). The second
  is the platform-specific instance of the first, with the same ground.
- **The automation disclaimer is mutually reinforcing.** C's
  `credential-contracts` block: *"Custody SHALL NOT be claimed to deliver
  automation."* C's `lifecycle-notebook-projection` block: *"A custody reference
  that implies unattended access the install does not have is worse than none."*
  B's archived § 8 explicitly does not claim unattended re-authentication, keeps
  `docs/notebooklm-sync-open-item.md` OPEN, and rides issue #537. Three
  statements, no drift.

## (d) Cross-references resolve; no contradiction, no orphan

**HOLDS.** Every reference carried by the twelve promoted blocks was extracted and
checked.

- **Path-shaped references: 1, and it resolves.**
  `scripts/sync-notebooklm-books.py` (`lifecycle-notebook-projection:145`) exists.
  Four further backticked strings match a path heuristic and are NOT paths, each
  verified in context: `*.template.yaml` and `*.example.yaml`
  (`credential-contracts:369-370, :433`) are glob patterns the text names in order
  to REFUSE them as an exemption basis; `credentials/` (`:305`) is a
  directory family inside a consuming DomainxFactory tree, not a path in this
  repository; `draft/` (`lifecycle-notebook-projection:351`) is an alias prefix
  the derivation strips.
- **Change-id references: 1, and it resolves.**
  `add-notebook-hosting-credential-custody`, in the `Modified over` marker, is
  written as a change-id code span rather than a path — it resolves through the
  change-id vocabulary to
  `openspec/changes/archive/2026-08-31-add-notebook-hosting-credential-custody/`.
  It did NOT become a dangling path when C archived, because it never was one.
- **Contract-token references: 14, all resolving.** Under `contracts/`:
  `xfactory_credential_binding_template` (4 files),
  `xfactory_credential_requirements` (1), `holder_ref` (43), `fetch_identity` (5),
  `requirement_ref` (4), `access_mode` (4), `shared_credential_acknowledged` (4),
  `credential_reference` (4), `secret_ref` (3), `credential_bindings` (5),
  `requirement_id` (99), `requirements_document_ref` (15). Outside `contracts/`:
  `managed_by` resolves to `scripts/sync-notebooklm-books.py` and
  `examples/lifecycle-notebook-workspaces.yaml`; the `consumer:` block resolves to
  `contracts/schemas/xfactory-credential-contracts.schema.yaml:185-229`, cut and
  published as `contract-v2.4`.
- **No contradiction was found between the three packets' promoted texts.** The
  one place where two promoted requirements pull in different directions is not a
  contradiction and is recorded below as **O-1**.

## (e) The marker and the amendment notes as historical records — ONE DEFECT

The `Modified over` marker at `credential-contracts:248` conforms to the reserved
form its authorizing change defines
(`openspec/changes/govern-sibling-added-modified-deltas/specs/document-lifecycle/spec.md:34`):
the basis is a code span, the `by` identifier is the change whose delta carries
the block, the date is present, and the required ` — <reason>` tail is nonempty.
Its survival into canon is the RULED DEFAULT, not a leak: that packet's OQ-2 —
*"whether a `Modified over` marker should survive promotion"* — is OPEN at its
`tasks.md` § 7.2, and the packet KEEPS the marker pending the answer. The
grammar itself is `ratified` and NOT YET CANON (that change is still active;
promoted `document-lifecycle` and `doc-health` each carry `Modified over` **0**
times), and doc-health's pairing arm reads ACTIVE changes only, so neither packet
is under it any more. C's `**AMENDED 2026-08-31**` strike note and D's § 7.4
re-measurement both read correctly against the promoted result: the strike is
absent from canon (a), and the six-in / six-out carriage is TRUE (b).

**F-1 — DEFECT, REPORTED AND NOT FIXED HERE: the marker's reason clause
undercounts, and three of the packet's own artifacts say otherwise.**

The promoted marker reads: *"this change is the successor that packet named
**three** times and could not perform itself."* Three artifacts of the same
packet say **five**, and one of them enumerates the sites:

| artifact | text |
| --- | --- |
| `…/2026-08-31-add-binding-consumer-identity/proposal.md:27` | *"the packet that ratified it said so **five times** — in its requirement's own scenario, its Impact section, its design, its task list §4.5 and its ratification record"* |
| `…/2026-08-31-add-binding-consumer-identity/review/ratification-2026-08-29.md:21` | *"It is the successor that packet named **five times** and could not perform itself"* — the same sentence as the marker's, with a different numeral |
| `contracts/schemas/xfactory-credential-contracts.schema.yaml:189-191` | *"the successor `add-notebook-hosting-credential-custody` named **five times** and could not perform itself"* — SHIPPED at `contract-v2.4` |

**And "three" is not a post-strike re-count either.** #538 struck exactly ONE of
the five sites — the requirement's own scenario — leaving **four**. So the
numeral matches neither the enumerated five nor the four that survive. It entered
with the marker itself (`20599623`, squash `3a6a16e9`, PR #538), whose § 6.1 and
§ 6.2 record the four markers written and the re-measurement occasioned, and
record no re-count of this figure.

The defect is a factual numeral in PROMOTED CANON that its own packet's proposal,
ratification record and shipped schema each contradict. **It is reported, not
repaired**: the text sits in canon and is mirrored in a closed archived delta, so
correcting it is an amendment act needing the ratifying owner's consent — the
same route § 6.2 of `govern-sibling-added-modified-deltas` took for the four
markers. It is not a dangling reference this record can note away.

**O-1 — OBSERVATION, NOT A CONTRADICTION: the singular custody pointer is a live
edge with no filed home.** C's promoted `lifecycle-notebook-projection:421`
requires the hosting record to carry *"a reference to the governed custody binding
that resolves it"* — singular — while D's promoted `credential-contracts:440`
makes a MULTI-CONSUMER record the normal case. These do not contradict: the
hosting record names a custody binding; D's plurality is about consuming systems,
and C's own `credential-contracts:237` already says revoking one binding is not
eviction. But D ruled the question (OQ-3) *"leave singular, route out — AND record
it as an owed successor WITH A NAMED HOME"*, and the home is named only as the
owning CAPABILITY (`design.md:782`, *"left to its owning capability"*). No issue,
no successor change, and no other document carries it: `grep -rn` for the
question outside D's own archive returns **0**. The security seat's caution —
*"a singular pointer beside a deliberately multi-consumer record resolves to one
binding, and an operator who follows it evicts one of two consumers believing
they evicted the access"* — is therefore live in promoted canon and lives only
inside an archived record. That is the same shape of residue #545 exists to
correct, and it is written down here so it does not stay there.

## What this record does not do

- It does not TICK C's § 6.2 or D's § 7.3. Those boxes are inside archived
  records; this record is their discharge, not their edit.
- It does not amend any of the three packets. Nothing under
  `openspec/changes/archive/**` was modified by the landing that carries this
  file, other than the addition of this file.
- It does not repair **F-1**, and it does not file **O-1**'s successor. Both are
  reported for the ruling that owns them.
- It does not re-verify B's own archive gate, C's or D's realization evidence, or
  any contract cut. Those were discharged by #539, #541, #516 and #526 and are
  cited rather than redone.

## Gates run for the landing that carries this record

- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — pass.
- doc-health, same clock (`--as-of 2026-08-31`), single-repo, against a baseline
  run at `origin/main` `4290cad2` — **zero new findings**. This file is inside the
  lifecycle scan set (`openspec/changes/**/review/*.md`, `scripts/doc_health/corpus.py:93`)
  and therefore carries `Status: record`, the stage every sibling record in this
  directory family carries.
- `python3 -m pytest tests/doc-health -q` — pass.
- The full suite is left to CI: this landing is documentation-only and touches no
  code surface.
