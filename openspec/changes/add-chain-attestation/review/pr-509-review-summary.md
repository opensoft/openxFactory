# PR #509 — council review summary, for the PULL REQUEST BODY

Status: record — **NOT A REVIEW RECORD, AND DELIBERATELY SO.**

**#509 gets no `review/` directory.** Brett Heap ruled ballot decision **10** on
2026-08-30: #509 lands by **ordinary pull request** with its appendix corrected.
`find ideation -type d -name review` returns **0** at `origin/main`; every review
record in this estate lives under `openspec/changes/<change>/review/`; and no
brainstorm vendoring here has ever carried one. **Creating one would invent a
convention this sitting has no authority to invent**, and `lead-architect`
independently ruled a council *"the wrong instrument"* for this subject.

**This file lives in the sitting's own home** — the combined sitting's physical
home is `add-chain-attestation/review/`, justified at that record's §5 — **because
it is a SITTING artifact, not a #509 artifact.** It is copy for the pull-request
body. **Nothing from this sitting is vendored into `ideation/`.**

Sitting: combined §7.4 council review, 2026-08-30, over PRs #510, #513 and #509.
Disposition of record: `disposition-2026-08-30.md` (this directory).
Seat returns, which GOVERN over this summary: `seat-returns-2026-08-30/`.

---

## THE BLOCK TO QUOTE IN THE PR BODY

> ### §7.4 council review — 2026-08-30
>
> This pull request was reviewed by a four-seat §7.4 council sitting
> (`gate_rules_council`, no-class shape) convened over three subjects on
> 2026-08-30, and **Brett Heap ruled on its ballot the same day**.
>
> **Verdicts — no refusal:**
>
> | Seat | Verdict |
> |---|---|
> | lead-architect | ACCEPT AS AMENDED |
> | lead-security | ACCEPT *(disclosure limb only — LS-C2)* |
> | lead-quality | ACCEPT AS AMENDED |
> | company-policy-lead | ACCEPT AS AMENDED |
>
> **What the bench found.** The vendoring is sound in kind, provenance-honest,
> lifecycle-conformant against the code that enforces it, and **doc-health clean
> — zero new findings, zero regressions**. `lead-security` confirmed it discloses
> **no credential, secret, key, PHI or identifier**, and that the unsafe 2024
> architecture it records is explicitly corrected in its own appendix so it cannot
> be read as endorsed. `company-policy-lead` called its dated section boundary
> *"a clean, reusable pattern for future vendorings."*
>
> **What must change.** The mapping appendix is **the one part of a brainstorm
> document that is not free-form**, and three seats independently checked it —
> 16, 17 and 4 targets respectively — and independently found the same core
> defects. **Brett's ruling accepts all three blocking amendments, rules LQ-C2,
> and folds this PR's open bot round into the fix round.** Brett's own speculative
> 2024 content is legitimate brainstorm material and is **not** being corrected;
> only the vendoring author's claims **about this estate** are.
>
> **No `review/` directory is created for this change** — brainstorm vendorings
> carry their review in the pull request, and this one does too.

---

## THE THREE BLOCKING AMENDMENTS — quote the return, not this summary

All three are `lead-quality`'s. **Verbatim from
`seat-returns-2026-08-30/lead-quality.md`.**

### LQ-A5 [509][513] — BLOCKING

> **LQ-A5 [509][513] — BLOCKING.** Correct "eighteen months" (LQ-F4). *Discharged
> by:* replacing it with the measured interval (**twenty-one months**, 2024-11-10
> → 2026-08-29) at #509 `:102` and `:207` **and** at #513 `spec.md:658-659`; or,
> in #513, striking the interval from requirement text entirely, since the
> requirement does not depend on it.

**Measured**: 2024-11-10 → 2026-08-29 = **657 days**. `company-policy-lead` found
this independently and traced the propagation into #513's own requirement text.
**Ruled decision 5 requires the #513 limb be carried too** — this is the one place
an error has already travelled from brainstorm colour into proposed contract text.

### LQ-A6 [509] — BLOCKING

> **LQ-A6 [509] — BLOCKING.** Correct the disposition label (LQ-F5). *Discharged
> by:* attributing the salted-keyed-commitment ruling and the erasure-by-salt-
> destruction property to **Q6** (`CONFIRMED … the ruling's OPERATIVE FORM`), and
> citing **Q2** (`ruled … AS RECOMMENDED`) for the boundary and the refusing
> validator — which is what each actually says.

The appendix at `:146` attaches Q6's stamp to Q2. **Found by all four seats.**

### LQ-A7 [509] — BLOCKING

> **LQ-A7 [509] — BLOCKING.** Remove or ground the two invented names (LQ-F6).
> *Discharged by:* deleting *"calls the commitments + anchoring pattern"* and
> *"calls chain inception's fidelity property"*, or replacing each with a phrase
> that resolves — e.g. claim 7's *"anchoring is multi-target and reversible by
> construction"*, and tranche one's requirement *"Ratification and chain inception
> are one signed act"* cited to the change rather than to the topic.

Both phrases return **0 hits repo-wide**, grep-verified separately by
`lead-architect`, `lead-quality` and `company-policy-lead`.

---

## LQ-C2 — RULED BY BRETT (decision 4). VERBATIM.

> **LQ-C2 [509].** The one existing imported brainstorm carries a standing
> disclaimer — *"These notes are imported evidence and idea material. They do not
> decide policy, memory, release scope, or OpenSpec approval."* #509 carries none.
> That is a precedent and not a contract, so I attach it as a condition rather
> than an amendment: **either carry the disclaimer or record that it was
> considered and declined.**

**RULED: either discharges it. Silence does not.** The fix round must **carry the
disclaimer text** — verbatim as quoted by the seat — **or record on the record
that it was considered and declined**, with a reason.

---

## THE FOLDED BOT ROUND — ruled decision 14, "14 folds into the fix rounds"

**All three bot reviews sit against `26c7e778`, #509's only commit. Every finding
is open.** Take or refute each **from the record with citations**.

| # | Finding | Bot |
|---|---|---|
| 1 | **P2 — "Limit verification to parties holding commitment secrets"** (`:133`). Under the Q2 architecture the appendix maps onto, the public value is a KEYED commitment whose salt stays in the governed layer, so *"a later holder with only the record and public anchor cannot recompute and verify it. This sentence carries over the public-verification property of a bare hash even though the privacy upgrade removes it."* Codex asks the claim be narrowed to an authorized verifier that can obtain the secret material while preserving the erasure policy. | Codex |
| 2 | **P2 — "Keep clinical access events distinct from the execution log"** (`:166`). The appendix claims the transparency log already retains granular access events, *"but the ratified requirement records only wallet ratification, chain inception, traveling-contract issuance, and gate verdicts"*; the mapping *"incorrectly makes required access-audit events appear implemented by the execution log."* **This independently corroborates the convening's own extrapolation finding** (ballot §X.3). | Codex |
| 3 | **P2 — "Require de-identification before treating metadata as reusable"** (`:190`). Querying MetaDataDB without PIIDB does not make a result de-identified; *"the repository's medical-data model explicitly requires a named Safe Harbor or Expert Determination de-identification gate (`docs/knowledge-lifecycle-model.md:131-134`), so describing this analysis lane as already supported could let tranche 3 bypass that privacy boundary."* **THIS ONE CROSSES: it is ALSO assigned to #513's fix round for its requirement-8 limb** (disposition §4). | Codex |
| 4 | **Q6 citation gap** (`:150`). The appendix says it *"ruled that topic's Q2, Q3, and Q6"* and cites by question anchors, *"but the body only cites Q2/Q3; Q6 is only mentioned in the intro."* | Copilot |

---

## SHOULD-FIX — not ruled item by item, and not covered by "accept all blocking"

`LA-A8` (the three mapping defects, LA's own formulation with a grep verifier) ·
`CPL-A1` (the interval) · `CPL-A2` (reword the two vocabulary attributions as the
appendix's own labels, not the topic's) · `CPL-A3` (the Q2 parenthetical) ·
`CPL-A4` (**reword the `Source:` block's fidelity claim to remove the "no content
reworded" / "not byte-identical" tension** — distinguish claims-preserved from
wording-reconstructed) · `CPL-A6` (align the header with the one imported-evidence
precedent's `Origin:` vocabulary, or extend `ideation/README.md`'s
imported-evidence provision to cover a non-NotebookLM import path).

**These are neither accepted nor rejected** — see disposition §6.

---

## ONE FURTHER CONVENING FINDING, UNRULED

`LQ-C3` names the defect class this subject exposed: *"a prose appendix asserting
facts about ruled dispositions and about what a document 'calls' something.
Three of them survived authoring, a bot round and the convening."* **No checker in
this estate reads it.** Recorded, not ruled, and not an obligation on this fix
round.
