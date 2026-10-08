# Proposal Ratification: refresh-install-repository-enumerations-opsxfactory-gateway

Status: ratified
Kind: report
Decision date: 2026-10-08
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-10-08 by Brett Heap (openxFactory operator authority) — in session on team-01b, first-hand to lane `openxfactory-5`, a multiple-choice answer, verbatim option label *"Ratify, OQs as recommended (Recommended)"*, given at about **20:2xZ** and logged RULED on the lane register at **2026-10-08T20:33:11Z**.
Ratified baseline: PR [#1273](https://github.com/opensoft/openxFactory/pull/1273)'s head **`114431d3`** (`114431d36189876ab679f34ddf3f81678619e392`), the head the pull request carried when the word was given. It was pushed at 2026-10-08T19:41:55Z and no commit came between it and the ratifying commit.

## Decision

**RATIFY, AS RECOMMENDED.** The packet stands as it was put: FIVE `## MODIFIED`
requirements across three capabilities, titles unchanged. The sixth install
repository, `OpsxFactory-Gateway-Install`, joins the install-repository
enumerations in `repo-boundary-governance` (three requirements, one paragraph
added carrying the gateway's admission record), `shared-contract-ownership` (one)
and `canonical-contract-migration` (one). Every widening is a list extension, each
replaced unit sits under a `Removed from canon` marker, and every other sentence
and scenario is carried byte-identically. `design.md` and `tasks.md` stand as
filed, with the dated notes of § 3.

**The word is a ratification only.** It is not a land word and not an archive
word. The pull request stays DRAFT, landing waits for a separate land word, and
the archive, which promotes the deltas, is a further act on a further word.
Nothing is promoted by this record, because `openspec/specs/` gains no byte until
the archive (`tasks.md` § 4).

**No code byte, pin, gitlink, contract bundle or release tag moves with this
record**, and no repository is created, admitted, renamed or re-pinned.

## 1. The word, and exactly what it decided

> Ratify, OQs as recommended (Recommended)

The lane recorded its reading of the option on the register as: ratify this
packet in DRAFT pull request #1273 with OQ-1 yes (the adapter family `Ops-gateway`
joins *"Contract breaks an adapter"*) and OQ-2 no routing scenario; the lane
encodes the ratification in the packet; landing, which archives it, waits for a
separate land word.

"As recommended" takes both recommendations the packet put, as written:

| OQ | decision | ruled answer | where it was put |
| --- | --- | --- | --- |
| OQ-1, the adapter family | does the gateway join `canonical-contract-migration`'s *"Contract breaks an adapter"* trigger? | **YES**: the adapter family `Ops-gateway` joins, and `specs/canonical-contract-migration/spec.md` stands | `proposal.md` § Two open questions; `design.md` D4; `tasks.md` 1.2 |
| OQ-2, the routing scenario | does the gateway get a routing scenario in *"Install repository scope"*? | **NO routing scenario**: the block keeps its three scenarios and the delta adds none | `proposal.md` § Two open questions; `design.md` D3; `tasks.md` 1.2 |

The alternatives stay rejected. Not joining (OQ-1) would delete one delta file and
leave the enumeration known to be one family short, with a later refresh owed when
the first adapter exists. Adding the scenario (OQ-2) would have settled what the
gateway's repository owns through an index, which the index requirement says an
enumeration does not do. The packet's other decisions (D1, D2, D5, D6, D7) put no
open question and stand as filed: five units widen and *"Submodule is proposed"*
needs no edit (D1), no active change collides (D2), the admission paragraph is a
paragraph of its own and the index requirement is left alone (D5), the `## Purpose`
widening is owed at the archive (D6), and no generator or checker is built (D7).

## 2. Why no delta byte moves

Every ruling is the recommended option, and the spec deltas already encode each
one. OQ-1 is the delta file `specs/canonical-contract-migration/spec.md`, which
stands. OQ-2 is the absence of a scenario, which is what the
`repo-boundary-governance` delta carries. So the three
`specs/*/spec.md` files are byte-identical to the text put to ratification.

## 3. What the ratifying commit moves

- `proposal.md`: `Status: ratified` with a `Ratified:` citation; a qualifier above
  the filing's "THIS PACKET IS A DRAFT" paragraph, which is kept verbatim as the
  filing's record; a RULED mark beside each of OQ-1 and OQ-2; the second word added
  to *The words, verbatim*; and the `## Ratification (pending)` section replaced by
  `## Ratification record` with the rulings table, the filed sentences quoted.
- `design.md` and `tasks.md`: `Status: ratified` with a `Ratified by:` citation.
  `design.md` gets a ratification qualifier above its opening paragraph, which is
  kept as filed, and a RULED mark on D3 and D4 with their reasoning kept.
  `tasks.md` ticks 1.1, 1.2 and 1.3 with the word cited, adds a note to 1.4 that
  the land and archive words are not given, and leaves 1.4, § 3 and § 4 unticked.
- `.openspec.yaml`: `approved_by` / `approved_on` are ADDED after `proposed_on`.
  `kind`, `id`, `reason`, `proposed_by` and `proposed_on` do not move.
- This record, and the README *Active changes* entry's status wording.

**Not moved:** the three `specs/*/spec.md` deltas, `tests/sequenced_after/corpus-ledger.yaml`
(the packet's row stays `state: active`, `class: co-modifier`) and every file under
`openspec/specs/`.

## 4. Encodings, and why

- **The origin pair is spelled `approved_by` / `approved_on`.** That is
  openxFactory's proposal-origin contract: its approval pair is
  `APPROVAL_FIELDS = ("approved_by", "approved_on")`
  (`scripts/doc_health/proposal_origin.py`), and an `ad_hoc` origin under
  `Status: ratified` without that pair is reported as an error. The pair is added
  in this ratifying commit, which is the first commit to declare `Status: ratified`
  anywhere in the packet, and it is added BESIDE the drafting provenance, the
  shape `add-drafted-proposal-origin` defined.
- **The instant is recorded to the precision the word was taken at and no finer.**
  The minute is written `20:2xZ`, the house form this repository's ratified
  packets use. The register's logging instant, 20:33:11Z, is recorded separately
  and as such.
- **This record carries `Status: ratified`, not `Status: record`.** `tasks.md` 1.3
  planned `Status: record`, and `document-lifecycle`'s scenario *A review record
  records a ratification* requires `Status: ratified` and one citation in a
  sanctioned spelling of a `review/` document that records that the change was
  ratified. The citation here is the record-citing `Ratified:` form, because the
  word is an in-session ruling and no approving OpenSpec change exists to name.
- **Boxes 1.1 to 1.3 are ticked, and 1.4 is not.** `tasks.md` § 1 is Brett Heap's
  acts. Each tick is made on his own recorded word, by the lane that encoded it,
  citing it. 1.4 is the land word and the archive word, which have not been given.
- **The citation is the lane register, not a pull-request comment.** The word was
  given in session and logged there, and the pull request body quotes the same word.

## 5. What is NOT done by this word

- **No promoted specification is edited.** The deltas are promoted by the archive
  act and by nothing earlier, and the archive is held for its own word.
- **The `## Purpose` widening stays owed at the archive** (`tasks.md` 4.1, in a
  hunk of its own, with the sentence quoted there).
- **openxFactory#1259 stays open.** It closes at the archive, by a word, and on no
  earlier pull request (`tasks.md` 4.2).
- **The pull request is not un-drafted and is not landed.** Rule 6, the landing
  window for a pull request touching `openspec/changes/` and the README OpenSpec
  Records block, applies at landing.
- **The estate repository inventory is untouched.** `scripts/estate-repository-inventory.yaml`
  carries no row for the repository; that is a named, unclaimed candidate and a
  code-surface edit under its own capability, as `tasks.md` 3.5 records.

## 6. Verification

Measured on the encoded tree, on top of PR #1273's head **`114431d3`**, against clean
`main` **`80f47483`** in a clone of the same kind: a full clone named `openxFactory`,
with the `openXwallet`, `openXdox` and `openDox` gitlinks CI's `pytest-suite`
initializes, so the repository identity and the skipped-family set match CI.

- **Pinned OpenSpec CLI** (`@fission-ai/openspec@1.12.0`, content address verified):
  - `--change refresh-install-repository-enumerations-opsxfactory-gateway --strict`:
    1 passed, 0 failed.
  - `--all --strict`: **115 passed, 1 failed (116 items), exit 0**, against clean `main`
    at 114 passed, 1 failed, exit 0.
  - The one failure is not this packet's: the `add-chain-attestation` exception that
    `contracts/openspec-cli-pin.yaml` already accepts.
- **House validators, each exit 0:**
  - `validate-sequenced-after.py .`;
  - `--ledger-diff`: "consistent with the corpus (236 rows)", and this record moves no
    ledger row;
  - `validate-code-surface.py .`;
  - `validate-target-release.py .`;
  - `proposal-support.py . verify refresh-install-repository-enumerations-opsxfactory-gateway`:
    "proposal support verification ok".
- **doc-health** (`scripts/doc-health.py --single-repo . --as-of 2026-10-08`): exit 0, and the
  finding set, sorted, is identical line for line to clean `main`'s (145 findings: 31
  critical, 26 error, 69 warning, 19 info). No finding names a file of this packet, this
  record included, in any family.
- **pytest, the full suite** (`python3 -m pytest tests/ -q -m "not postgres"`, CI's
  `pytest-suite` command): **38 failed, 9171 passed, 7 skipped**. The 38 failing test ids are
  IDENTICAL to the 38 measured on clean `main` in the same clone kind, and none names this
  change. They are environmental: the scratch directory this run used sits inside an
  aggregation git work tree, so the tests that assert "not a git work tree" and path
  resolution outside one fail on `main` as they do here. The same counts held at the packet's
  opening head.
- **Spec deltas:** `git diff 114431d3 -- openspec/changes/refresh-install-repository-enumerations-opsxfactory-gateway/specs`
  is empty.
