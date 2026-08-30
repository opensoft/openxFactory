# MedxChain — Blockchain-Backed Medical Record Fidelity — Brainstorm

Status: brainstorm
Kind: reference
Summary: MedxChain is Brett Heap's original 2024 design sketch for a
blockchain-backed medical-records product: on-chain hashes give a record a
notarized, tamper-evident fidelity proof, three segregated databases keep
identifying data, clinical data, and access-control data apart, and every
access is logged immutably for HIPAA audit compliance.
Topics: medxchain, medxfactory, blockchain, medical-records, hipaa,
record-fidelity, signed-execution-chain, healthlinc
Repository context: openxFactory neutral ideation; maps onto the staged
signed-execution-chain topic and the MedxFactory domain
Captured: 2026-08-29

Source: Brett Heap's original MedxChain design notes, authored 2024-11-10
(OneNote). Shared into this pipeline 2026-08-29 and vendored here from Brett
Heap's notes via session transcript — structure and claims preserved,
formatting normalized from OneNote export artifacts only (page footers,
orphaned bullet/number fragments, and duplicated headers stripped) — no
content reworded. The OneNote original remains the source artifact of record
for exact wording; this vendoring reconstructs the notes' section structure
and enumerated claims from that transcript rather than reproducing
byte-identical prose.

These notes are imported evidence and idea material. They do not decide
policy, memory, release scope, or OpenSpec approval.

## Overview

MedxChain was sketched under three candidate names/domains: myHIPPAA.com,
HappyHIPPAA.com, and HIPPAA.org — a patient-facing product built around
compliance with "HIPPAA" [sic — the deliberate backronym; the statute is
HIPAA], expanded in the notes as "Health Information Patient Plan Analysis
and Audit". The product idea: give patients and providers a way to prove a
medical record has not been tampered with, without putting the record itself
anywhere public.

## Record Fidelity

- **Initial verification**: a record is hashed and the hash is timestamped
  on chain at creation.
- **Ongoing verification**: the same hash is recomputed and compared against
  the on-chain value at any later point to prove the record is unchanged.
- **Digital-notary benefits**: the chain plays the role of a notary — it
  does not hold the record, it holds proof the record existed in a given
  state at a given time.
- **"One-time access to create the hash, verify indefinitely"**: the
  record only needs to be touched once, at hashing time; after that, the
  hash on chain lets anyone with a copy of the record verify it forever,
  without further access to the original.

## Security Architecture

- **Medical Records DB**: stored off-chain; only its hash goes on chain.
- **Metadata DB**: stored off-chain; only its hash goes on chain.
- **PII Database**: entirely on the blockchain, encrypted. It carries
  patient identifiers, links to the corresponding record hashes,
  access-control lists (ACLs), timestamps, and signatures.
- **Per-access blockchain entries**: every access to a record produces its
  own blockchain entry, so the PII Database's on-chain trail is also the
  access log.

## Blockchain Logging

- **Immutable audit trail**: the chain gives an audit trail nobody —
  including an administrator — can quietly edit after the fact.
- **HIPAA audit compliance**: this immutability is positioned as satisfying
  HIPAA's audit-trail requirements directly.
- **Logged events**: views, edits, failed access attempts, and
  administrative actions are all logged on chain.

## Database Architecture

Three databases, deliberately segregated:

- **RecordDB**: the encrypted medical records themselves — `RecordHash`,
  `EncryptedData`, and timestamps. Carries **no patient identifiers**.
- **MetaDataDB**: `RecordHash`, age, gender, and other clinical data
  suitable for meta-analysis. Carries **no PII**.
- **PIIDB**: `PatientID`, `RecordHash`, `MetaDataHash`, and access-control
  data, held at the highest encryption level of the three databases.

**Benefits of the split**: clinical meta-analysis can run against
MetaDataDB (and RecordDB) without ever exposing PII; patient care is served
by the linkage the hashes preserve; and the segregation minimizes
breach risk — compromising one database does not, by itself, expose
identity, clinical detail, and access control together.

## Access Control Logging / Three-Part Storage

- **Encrypted MRI data in IPFS**: large imaging data (MRI) is stored
  encrypted in IPFS rather than in a database.
- **IPFS hash on blockchain**: the IPFS content hash is anchored on chain
  along with a timestamp, a signature, and modality metadata (what kind of
  imaging study it is).
- **Timestamping process**: the on-chain timestamp is what lets a later
  verifier establish exactly when the imaging data was committed.
- **Access control with per-attempt logging**: every access attempt to the
  IPFS-stored data — not only successful ones — is logged, consistent with
  the Blockchain Logging section's "failed attempts" event class.

## How MedxChain meets the signed-execution-chain architecture — 2026-08-29

MedxChain is Brett Heap's own 2024 design sketch, arriving twenty-one months
before the `signed-execution-chain` topic's 2026-08-29 clarify sitting ruled
that topic's Q2, Q3, and Q6. Read together, MedxChain is an early,
domain-specific instance of the same shape that topic later worked out
neutrally — and the ruled dispositions both validate MedxChain's instincts
and correct three places where 2024-era assumptions no longer hold. This
appendix cites `ideation/staging/signed-execution-chain/signed-execution-chain.md`
by its section and question anchors; it does not restate that topic's
reasoning.

### Convergences

- **Hash-fidelity / digital notary** (Record Fidelity, above) is the same
  commitment-and-anchor design `signed-execution-chain` sets out in its
  "The on-chain layer, as ruled" section and claim 6: a chain does not hold
  the record, it holds proof the record existed unchanged.
- **Bytes off-chain, handles on-chain** (Security Architecture: Medical
  Records DB and Metadata DB off-chain, hashes on chain) is exactly the
  boundary `signed-execution-chain` draws under Q2: "off chain: every
  payload without exception... on chain: salted keyed commitments... and
  the chain anchors."
- **Three-database segregation** (Database Architecture: RecordDB /
  MetaDataDB / PIIDB) is the same move as `signed-execution-chain`'s
  **plane separation** — off-chain encrypted custody, a governed
  permissioned layer, and an on-chain anchor layer, each holding a
  different kind of fact (see its "So the split is" table).
- **"One-time access to create the hash, verify indefinitely"** (Record
  Fidelity) echoes, at a much smaller scale, the one-time signed act that
  `add-signed-execution-chain` — the ratifying CHANGE, not this staged
  topic — names **chain inception** (its Requirement: Ratification and
  chain inception are one signed act,
  `openspec/changes/add-signed-execution-chain/specs/signed-execution-chain/spec.md:151`):
  a commitment, once anchored, lets a later authorized verifier that holds the
  record and can obtain the governed commitment secret verify it without
  further access to the original source or to the party that committed it. The
  privacy upgrade deliberately removes the public recomputation property of a
  bare hash.
- **Access logging** (Blockchain Logging; Access Control Logging) foreshadows
  a Medx clinical-use event family that can use the same signed, append-only
  and checkpointed evidence pattern. It is not already covered by the current
  signed-execution-chain transparency log, whose ratified event family concerns
  factory execution rather than patient-record views, edits, and failed access
  attempts.

### The three 2026 upgrades MedxChain's design needs

Three places where the ruled topic's evidence-based corrections move past
what MedxChain's 2024 sketch assumed:

- **Plain hashes → salted keyed commitments.** MedxChain's Record Fidelity
  and PII Database sections describe anchoring plain hashes. Q2, ruled
  2026-08-29 (AS RECOMMENDED), draws the boundary and requires **salted
  keyed commitments**, never bare hashes, because
  [EDPB Guidelines 02/2025 (v2.0)](https://www.edpb.europa.eu/system/files/2026-07/edpb_guidelines_202502_blockchain_v2_en.pdf)
  hold that a hash of personal data is itself personal data. Q6,
  CONFIRMED 2026-08-29 as the ruling's **OPERATIVE FORM**, attaches
  **erasure by salt destruction** as the erasure mechanism for that
  commitment reading — a property a plain hash cannot offer — and confirms
  it applies to patient-anchored PHI portions; it is not permission to
  publish PHI, ciphertext, or plain record hashes.
- **PIIDB "entirely on the blockchain, encrypted" → a permissioned consent
  plane with anchored state roots.** MedxChain's Security Architecture
  puts the whole PII Database, encrypted, on a public chain. Q2's ruled
  boundary excludes this outright: encrypted PHI on a public ledger is
  still refused, because a public chain cannot forget — the ciphertext is
  permanent and key management becomes the only thing standing between a
  patient and disclosure, forever. The ruled architecture instead keeps
  consent state and identifiers in a **governed permissioned layer**,
  anchoring only that layer's **state roots** and consent-log
  **checkpoints** publicly (see "What goes on chain, and what must not").
- **Per-access public blockchain entries → signed log entries with
  batched anchored checkpoints.** MedxChain's "per-access blockchain
  entries" (Security Architecture) and per-event logging (Blockchain
  Logging) put every view, edit, and failed attempt directly on a public
  chain. A future Medx clinical-use event family should keep this granular
  signed log off chain and anchor only **batched checkpoints** publicly. It
  may compose with the neutral checkpoint and receipt pattern, but it remains
  distinct from the current factory-execution transparency log. This avoids
  both the metadata leakage of publishing every access event to a public
  ledger and the cost of anchoring at that granularity.

### The ruled anchoring configuration it inherits

Any future MedxChain build inherits Q3's ruled configuration (ruled
2026-08-29, two rounds) rather than re-deriving chain selection: **Kaspa
first**, as the primary, operational witness, adopted under the
chain-selection study's three conditions (archival node; inclusion proofs
captured and retained at anchor time; corroborating evidence, never sole);
**Bitcoin via OpenTimestamps aggregation on every anchored item**, as the
durability witness — ten-year claims cite Bitcoin; **no selectivity**
(no per-item judgement about which items get a Bitcoin anchor); and **no
third chain**.

### What MedxChain adds to carry into tranche 3

MedxChain's notes carry two ideas the `signed-execution-chain` topic's
current text does not yet name, and one framing worth stating explicitly:

- **The meta-analysis lane.** MedxChain's Database Architecture section
  makes RecordDB-plus-MetaDataDB, queried without PIIDB, a first-class use
  case. Segregation from PIIDB does **not** by itself make age, gender,
  clinical data, or linkable record hashes de-identified. Any meta-analysis
  consumer must first pass the named Safe Harbor or Expert Determination gate
  required by `docs/knowledge-lifecycle-model.md`; until then this is sensitive
  governed data, not a reusable de-identified corpus. `signed-execution-chain`'s
  tranche 3 does not yet name this possible consumer, and should carry it only
  with that formal gate and the applicable consent and purpose controls.
- **Verification-attempt auditing, not just writes.** MedxChain's
  Blockchain Logging section logs "failed attempts" alongside views,
  edits, and admin actions — auditing verification and access ATTEMPTS,
  not only successful writes. `signed-execution-chain`'s ten links are
  framed around what was signed and produced, so the neutral hook
  tranche 3's contract text should carry explicitly is a generic
  verification-ATTEMPT scenario alongside the successful-access case —
  not MedxChain's own patient-record access and failed-access-attempt
  logging, which is the domain-specific clinical audit case named above
  (Medx clinical-use event family) and routes to the HealthLinc/
  MedxFactory domain realization, not into this neutral family's
  contract text.
- **MedxChain as the MedxFactory-domain instantiation.** `signed-execution-chain`'s
  claim 2 names **HealthLinc** as the patient-facing app through which a
  ratified treatment plan is "merged" (pushed to the patient app, or
  printed as signed orders). MedxChain is best read as an early sketch of
  that same HealthLinc surface, predating the neutral family by twenty-one
  months. Claim 3's **LedgerLinc** is the financial-records analogue over
  the same chain shape, per claim 4's "two mappings are the same shape"
  argument.

### IPFS note

MedxChain's Access Control Logging section anchors an IPFS content hash on
chain for encrypted MRI data. The ruled architecture subsumes
content-addressing generically under its commitment scheme (a salted keyed
commitment IS a content-addressed reference, with the added erasure
property a bare content hash lacks) — so IPFS is not a separate primitive
to carry forward, it is one instance of "bytes off-chain, handle on-chain."
The same caution Q2 raises about public anchoring applies to public IPFS
pinning of encrypted PHI: a publicly pinned encrypted blob is still
permanent and still carries the cannot-forget problem. A governed store
holding the encrypted imaging data, referenced by a content-addressed
handle whose salted commitment is anchored, gives MedxChain's IPFS idea the
property it wanted without the public-pinning exposure.
