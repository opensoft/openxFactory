# openxVault — Git-Native Record Vault — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Pull the PHI out of OpenSpec-governed document management and
store it in SOPS-encrypted, KMS-audited files — the combination of the
sanitized analysis plane, a commodity bulk plane, and the encrypted vault
plane is a basic document-EMR (and CPA-grade client vault) built on the
custody-tier model, with de-identified records reusable for research.

Naming (decided by Brett, 2026-07-16): **openxVault** — the neutral
custody/storage capability (planes, custody tiers, encryption ladder,
sanitizer, evidence manifests), following the family's
neutral-contract → domain-instantiation pattern (MedxVault,
LedgerxVault, ... when adopted). Identity, credentials, and capability
grants are the sibling capability **openxWallet**
([agent-certification-wallets.md](agent-certification-wallets.md)); the
vault's gate CONSUMES wallet grants — that boundary is the split between
the two names.

Topics: openxvault, custody, storage, phi, sops, kms, encryption-tiers,
sanitizer, analysis-plane, vault-plane, de-identification, document-emr
Repository context: openxFactory (neutral openxVault capability)
Origin: 2026-07-15 session with Brett, growing out of the
ideation-dashboard brainstorm's custody-tier section ("Custody tiers: git
as the traceability plane") — this doc gives the vault idea its own
lifecycle path. Being brainstorm-stage, items may contradict; nothing
here is normative.

## Possible feats

- **openxVault neutral custody capability** — planes, custody tiers, encryption
  ladder, sanitizer, evidence manifests.
- **Sanitized analysis plane + encrypted vault plane** split for PHI-bearing docs.
- **De-identified commodity bulk plane** reusable for research.

## The insight

If the sanitizer (custody-tier hard rule 3) pulls PHI out of governed
docs and that PHI is stored in SOPS-encrypted files, the system becomes a
basic EMR: pseudonymized docs stay fully analyzable (dashboard,
NotebookLM, catalog — all existing machinery), while the
pseudonym→identity map and protected field values live encrypted,
versioned, and hash-locked in git. Structure visible, values opaque,
every change audited.

## Three planes (Brett, 2026-07-15)

1. **Git evidence/governance plane** — manifests, sanitized/pseudonymized
   docs, analyses, decisions. GitHub-hosted; full dashboard + NotebookLM
   treatment; the traceability plane from the custody-tier model.
2. **Commodity bulk plane** — because PHI is separated, LARGE files
   (imaging, scans, exports) live in ordinary blob storage + a database
   with no PHI custody burden: cheap, unencumbered infrastructure.
   Content-addressed (hash-named) so evidence manifests reference exact
   bytes; git never holds big binaries. And since the records there are
   de-identified, they are reusable for RESEARCH and secondary analysis —
   the de-identification that protects patients also unlocks the data.
3. **PHI vault plane** — SOPS-encrypted files (identity maps, protected
   values, the sanitizer's engagement salts/HMAC keys) on self-hosted git
   inside the clinical boundary. The crown jewels, smallest possible.

Salted hashes chain all three planes: opinion → sanitized inputs (plane
1) → bulk artifacts (plane 2) → (inside the boundary only) identity
(plane 3).

## Four design choices that make it defensible

1. **KMS-backed SOPS master keys, never local age/PGP.** Git logs writes;
   an EMR must audit READS. KMS-backed keys make every decrypt a
   centrally logged, revocable API call — upgrading SOPS from "encrypted
   files" to "access-audited records."
2. **One SOPS file per patient/record → crypto-shredding.** SOPS uses a
   per-file data key; per-record files mean erasure = destroy that
   record's key, and the ciphertext across all git history becomes noise.
   Resolves git-immutability vs right-to-erasure — but only if file
   granularity is right from day one.
3. **Ciphertext placement.** Encrypted PHI is still ePHI; hosting even
   ciphertext on a non-BAA service is a gray zone. Plane 1 on GitHub;
   plane 3 on self-hosted git (Gitea/GitLab) inside the boundary.
4. **The EMR "brain" already exists.** Consent, approval, break-glass,
   erasure, and audit are Hermes's job, and the memory-gateway contract
   family already carries erasure/break-glass/audit vocabulary — this is
   those contracts applied to a SOPS vault instead of a memory store.

## Sensitivity locus and the purpose-driven encryption ladder (Brett, 2026-07-15)

General rule: **for secure documents, the identity/linkage always goes to
the encrypted vault (plane 3). Whether the FILES themselves are encrypted
is then decided by sensitivity locus and purpose.**

**Locus 1 — linkage-sensitive** (medical, legal clients, financial
accounts): the danger concentrates in WHO the record is about, not the
content itself. Identity → vault; content tiers by purpose:

| Rung | State | Purpose / access |
|---|---|---|
| (a) | Fully encrypted, identified | the raw record; vault-plane custody, clinician/key-holder only |
| (b) | **Encrypted after de-identification** | controlled research: the dataset gets its own SOPS/KMS data key issued to a named researcher group — trust moves from the storage to the key, so commodity blob/DB still works |
| (c) | De-identified, plaintext | public/open research — REQUIRES the formal de-identification bar (Safe Harbor or Expert Determination), not just pseudonymization |

Refinement of the three-plane note above: plane 2's "no PHI custody
burden" applies fully only to rung (c); rung (b) data rides the same
commodity storage BECAUSE it is encrypted, not because it is harmless.

**Locus 2 — content-sensitive** (high-security engineering, trade
secrets): the danger is diffused through WHAT the document says; there is
nothing meaningful to de-identify, so a half stage buys nothing
(Brett: "if you decrypt, you see all — I do not see value in a half
stage"). Binary custody: encrypted whole, access by clearance. Noted as
policy default rather than technical constraint: per-file SOPS keys still
permit need-to-know compartments (per project/cell) later without
redesign.

**Locus 3 — open** (codex governance docs and most engineering work):
plaintext, repo-native — the existing tier-1 custody, unchanged.

The dashboard/NotebookLM consequence: the custody profile per repo/source
gains a locus + rung declaration, and the NotebookLM dispatch gate reads
it — rung (a) never dispatches, rung (b) dispatches only under the
dataset key-group's authorization, rung (c) and locus-3 dispatch freely.

## Research-reuse caveats (honest edges)

- Salted-pseudonymized data is "coded," not Safe-Harbor de-identified:
  while the key exists, the key-holder org can re-identify. Internal
  research use is the normal case; external sharing needs formal HIPAA
  de-identification (Safe Harbor's identifier removal or Expert
  Determination). Record which bar each dataset clears.
- Imaging carries embedded PHI: DICOM headers, burned-in annotations on
  scans/PDFs. The sanitizer must scrub file METADATA and pixels/text
  layers, not just document prose, before anything lands in plane 2.
- The sanitizer itself is a bounded Omnigent lane (same shape as the
  document-cataloger) and inherits the model-worker contract lessons:
  the model emits judgment; orchestration computes every hash and
  pseudonym.

## Patient wallet: capability grants over the vault (Brett, 2026-07-15)

The patient holds their records in a "medical wallet" and issues scoped,
time-boxed access to professionals. Cardinal rule: **never hand out raw
keys** — raw keys cannot expire or be revoked. The wallet holds a SIGNING
key; access travels as attenuated capability grants.

- **Wallet** = a device-bound signing key (passkey/WebAuthn for real-user
  UX — no seed phrases) anchored to a DID, holding (1) the patient's own
  linkage-salt share (a patient can always re-identify their own records;
  the org still needs the vault) and (2) the root capability over their
  record set.
- **Grant** = a signed capability token (UCAN/Biscuit/macaroon-style
  attenuation, or a W3C Verifiable Credential): audience = the
  professional's DID; records = evidence-manifest salted hash refs (the
  grant never names content); scope = locus rung + purpose; expiry;
  optional single-use. Issued as QR/link — the SMART Health Cards/Links
  interaction pattern, proven at population scale.
- **Enforcement fork**: (v1, recommended) KMS-mediated — the Hermes-gated
  vault API verifies the grant, logs it, and releases a short-lived
  derived key scoped to it; revocation and expiry are actually
  enforceable; trust = the vault operator, which is already true.
  Upgrade paths: proxy re-encryption (ciphertext transformed to the
  grantee's key without plaintext exposure) and threshold split-key
  (patient share required for any decrypt — maximal sovereignty, but
  patient unavailability becomes a clinical availability problem, so
  break-glass is required by construction).
- **Every grant/use/revocation/break-glass event is itself a governance
  record** committed to the evidence plane (DIDs + hashes only, PHI-free):
  "who could see what, when, granted by whom" lands in the same
  traceability plane as "which bytes produced this diagnosis."
- **Break-glass** is not new design: the memory-gateway contract family's
  break-glass/audit vocabulary applied to the vault.
- **Steal, don't invent**: UMA 2.0 / HEART profile (purpose-built
  patient-directed health-data sharing), SMART on FHIR scope vocabulary,
  W3C DID/VC, UCAN/Biscuit for attenuation. Blockchain not required —
  git + KMS logs already provide the tamper-evident audit; a ledger
  anchor stays optional.

**Practitioner wallets (Brett, 2026-07-15): both ends of every grant are
wallet-held keys.** Practitioners carry the same passkey-backed DID
wallet, which upgrades three things at once:

1. **Possession-bound grants**: using a grant requires proof-of-possession
   (a signature from the practitioner's wallet key), not mere bearer
   presentation — a stolen grant is useless without the key.
2. **Key-attributed views**: every KMS-mediated decrypt logs the
   practitioner's key alongside the grant — cryptographic attribution for
   the classic EMR snooping/audit problem, instead of shareable logins.
3. **Signed edits**: amendments and notes are APPEND-ONLY commits signed
   by the practitioner's key (git commit signing, or the record appended
   as a signed VC) — never rewrites, matching the medical-legal
   right-to-amend model, non-repudiable, landing in the same evidence
   plane as everything else.

Falls out for free: **licensure as wallet credentials** — the
practitioner's DID carries verifiable credentials (medical license, DEA,
CPA for Ledgerx) that the vault gate verifies ("licensed, current")
before honoring any grant; and **attenuating delegation chains**
(attending → resident → nurse, each link narrowing scope/time, every
link signed), with the patient's original grant able to carry a
no-re-delegation caveat.

Additional OQs this raises: wallet recovery/custodianship (lost phone;
minors; incapacitated patients — custodial fallback degrades gracefully
to today's practice-held model); grant granularity (whole record set vs
per-encounter vs per-document); the professional trust registry (who
issues licensure VCs and how revocation of a LICENSE propagates to live
grants); delegation policy defaults (re-delegable or not, and who
decides).

## Scope line

This is a **document-EMR — a governed records vault** — not a clinical
workflow system (no orders, e-prescribing, HL7/FHIR, scheduling). Where a
practice has a real EMR, that stays the tier-2 system of record and this
changes nothing. The vault serves contexts WITHOUT one: small practices,
consulting/second-opinion engagements, expert-analysis workloads — and
the identical pattern gives LedgerxFactory a CPA-grade client vault
(engagement branches, hash-locked PBCs, tagged opinions).

## Open questions

- **Vault repo topology**: one vault repo per client/patient panel vs one
  per engagement? (Crypto-shred granularity and key-group blast radius
  pull in opposite directions.)
- **Plane-2 store**: plain object storage + content hashes vs a
  content-addressed store (e.g. LFS-adjacent or OCI registry) — what does
  the manifest reference format commit to?
- **Key custody**: which KMS, whose tenancy, and where do engagement
  salts rotate? (Hermes credential-contract territory.)
- **Research egress gate**: who approves a plane-2 dataset for a research
  use, and is that a Hermes gate like every other approval?

## Exit

Organize into a staged topic once the open questions carry
recommendations. Likely exits as an openxFactory contract change (vault
custody + evidence-manifest schemas + sanitizer worker contract,
generalizing the document-cataloging redacted-dispatch rule) paired with
MedxFactory/LedgerxFactory adoption deltas — same two-repo split as
document-cataloging. Cross-reference: the custody-tier and sanitizer
sections in [ideation-dashboard.md](ideation-dashboard.md).
