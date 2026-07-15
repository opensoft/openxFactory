# Git-Native Record Vault — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Pull the PHI out of OpenSpec-governed document management and
store it in SOPS-encrypted, KMS-audited files — the combination of the
sanitized analysis plane, a commodity bulk plane, and the encrypted vault
plane is a basic document-EMR (and CPA-grade client vault) built on the
custody-tier model, with de-identified records reusable for research.

Origin: 2026-07-15 session with Brett, growing out of the
ideation-dashboard brainstorm's custody-tier section ("Custody tiers: git
as the traceability plane") — this doc gives the vault idea its own
lifecycle path. Being brainstorm-stage, items may contradict; nothing
here is normative.

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
