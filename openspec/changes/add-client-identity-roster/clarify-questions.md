# Clarify round — add-client-identity-roster (2026-08-14)

Status: record
Round: 1. Five questions. Q1–Q4 are the ratify-gate decisions (tasks.md 1.2,
expanded); Q5 emerged while writing the surface vocabulary. Answers are
recorded inline here and applied to `proposal.md` / the spec delta / `tasks.md`.

Context for every question: the cross-model review record
(`review/decision-review-2026-08-14.md`) and the rejected alternatives in
`design.md`. The measured basis is the Business Central admission chain
(`xFactories/OpsxFactory/tenants/farheap-bc-sandbox1-verify-probe-evidence-v3..v7`).

---

## Q1 — Does the residency default bend by authority class?

Drafted: client-resident single-tenant for ALL governed identities;
vendor-tenant-multi only through the governed model with full obligations
(tenant allow-list at token validation, per-client authorization state and
revocation evidence, cross-client credential-span statement, consent
amendment per affected client).

- **(a) Class-independent (as drafted, recommended)** — client-resident is
  the default regardless of class. Safest; most expensive; per-client
  enrollment for every surface.
- **(b) Class-dependent** — vendor-tenant-multi permitted by default for
  `observe`, client-resident required for `mutate`. This is where the real
  cost relief is. Honest counterweight: an observe-class multi-tenant
  compromise yields READ across every consenting client's governed surfaces
  — ERP data, documents, mail. "Read-only" is not benign at that span.
- **(c) Vendor-tenant-multi as the default everywhere** with the obligations
  attached. Cheapest; matches the already-decided ISV/connect-app shape;
  largest blast radius.

Note: LedgerxFactory's ratified naming registry already assigns its
Reader/Poster to a **multi-tenant pair**, so (a) makes this contract's
default differ from a sibling domain's shipping architecture — deliberate,
but worth naming.

**ANSWER:**

---

## Q2 — Blocking scope, and is the grant-issuance refusal in THIS change?

Drafted: intra-repo entry conformance BLOCKS the owning domain's gate;
cross-domain composition REPORTS via doc-health; and an open drift finding
REFUSES grant issuance for that identity.

- **(a) All three, as drafted (recommended)** — the refusal is the one lever
  we own that is not a mutation of the client's estate.
- **(b) Split the refusal out** — keep blocking/reporting here; make the
  grant-issuance refusal its own successor change. Smaller blast radius for
  this contract; leaves a window where a drifted identity keeps receiving
  fresh JIT credentials.
- **(c) All advisory** — nothing blocks, everything reports. Least
  disruption to existing gates; guts the traceability requirement (a
  `mutate` identity with no ratified capability becomes a nightly warning).

**ANSWER:**

---

## Q3 — Enrollment obligation sequencing

The axis is deliberately permissive (per-unit and per-duty identities
allowed), which is safer and more expensive. Automation is refused on
principle. The entry lifecycle (`planned|enrolled|retired`) softens timing,
not total cost.

- **(a) As drafted (recommended)** — ratify the axis; entries may sit
  `planned` indefinitely; no obligation to enroll a full set at once.
- **(b) Add a minimum-viable-enrollment rule** — one `observe` entry per
  governed surface at enrollment; every `mutate`, per-unit and duty identity
  arrives on demand with its capability. More prescriptive, more predictable
  client-side footprint.
- **(c) Defer domain fragment obligations** until a second paying client
  exists (a single-client estate does not exercise composition anyway).

**ANSWER:**

---

## Q4 — Does this change land contract-only, or with its two MODIFIED realizations?

The rewrite made the change honestly MODIFY `consent-instrument` (termination
cascade reaches identities and their provider-side admission) and `doc-health`
(sixteenth family). Both need realization work.

- **(a) Contract + both wirings (recommended)** — schema/validator/examples
  plus the consent cascade plus the doc-health family; archives complete.
- **(b) Contract-only** — cascade and family become named successors. Lands
  faster; the cascade gap stays open meanwhile (withdrawal revokes a
  credential while the identity keeps standing, still admitted).
- **(c) Contract + consent cascade; defer the doc-health family** — closes
  the withdrawal gap now; the cross-domain check waits, which costs little
  while there is one client.

**ANSWER:**

---

## Q5 — First-release scope of the closed `admission_surface` vocabulary

- **(a) Only surfaces with a ratified capability today** — Business Central
  and Exchange. Smallest, most honest; every other surface arrives with its
  capability.
- **(b) All Entra-homed M365 + D365 surfaces now** (BC, Exchange,
  collaboration/content, Dataverse/CRM) — declares the intended product
  footprint up front; risks vocabulary written ahead of measurement, which is
  the failure mode this whole change exists to prevent.
- **(c) Include non-Entra providers now** (client-org GitHub App
  installations) — reconciles with `client-infrastructure-liaison`
  immediately rather than as a named successor.

**ANSWER:**
