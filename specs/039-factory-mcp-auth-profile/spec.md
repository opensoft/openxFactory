# Feature Specification: Factory MCP authorization profile

**Feature Branch**: `039-factory-mcp-auth-profile`
**Created**: 2026-10-09
Status: draft
Kind: reference
Governed by: [amend-factory-mcp-conformance-auth-profile](../../openspec/changes/amend-factory-mcp-conformance-auth-profile/proposal.md), ratified 2026-10-08 (record [`review/ratification-2026-10-08.md`](../../openspec/changes/amend-factory-mcp-conformance-auth-profile/review/ratification-2026-10-08.md)); its packet landed as pull request #1274 (`93d13d6c`).
**Input**: the change's `tasks.md` § 2, "Realization (one Speckit feature)": the authorization block on a deployed factory MCP declaration (issuer, an RS256 baseline with optional EdDSA, the audience and its binding, the RFC 9728 metadata path, and an `auth` support concern), the M5 narrowing of *Unavailable dependency* to error-inventory codes, and per-domain error vocabularies.

## Authority and traceability

This feature realizes one ratified delta,
[`specs/factory-mcp-conformance/spec.md`](../../openspec/changes/amend-factory-mcp-conformance-auth-profile/specs/factory-mcp-conformance/spec.md)
of the change: four `## ADDED` requirements (16 scenarios) and one
`## MODIFIED` requirement (3 scenarios). The ratified text is the authority.
The requirements below index it and add only what the realization must decide
where the change's [`design.md`](../../openspec/changes/amend-factory-mcp-conformance-auth-profile/design.md)
leaves that to it. They never restate a scenario differently. Every
requirement names the delta scenario and the design decision it traces to, and
[`tasks.md`](tasks.md) names the test that witnesses it.

The feature amends the conformance surface that
[feature 037](../037-factory-mcp-conformance/spec.md) built: the declaration
schema, its validator, its tests and its runbook.

## Clarifications

### Session 2026-10-09

No question was asked. The clarify scan found nothing the ratified packet
leaves materially open. Brett Heap ratified the packet as drafted and took all
six of `design.md`'s open questions (OQ-1 to OQ-6) at the recommended answer,
and the lane's coordinator accepted this no-question verdict when it resumed
the seat (2026-10-09T17:2xZ). Every remaining choice is either delegated to the
realization by the packet or settled by a standard the packet cites. Each one
is recorded in [`research.md`](research.md) with the line that decides it:

- the block's field names (`design.md` D1: "field names are the realization's
  to confirm"), kept exactly as D1 proposes;
- whether a structural fault inside the block names its field (`design.md` D7:
  "This packet does not choose"). It does not: `tasks.md` 2.2 expects
  `schema_oneOf` at `/service`;
- what counts as a query component (RFC 3986 § 3) and whether a token-signing
  algorithm name is case-sensitive (RFC 7515 § 4.1.1);
- how the new checks combine with the existing `invalid_resource_uri` check,
  which the packet's code table leaves to the semantic pass's existing rules.

**Feature creation.** Speckit's `before_specify` hook (`speckit.git.feature`)
was not run. In this repository it creates a sibling worktree under
`../openxFactory-worktrees/`. This feature was assigned an isolated full clone
on the branch `039-factory-mcp-auth-profile`, made from `main` at `93d13d6c`,
by the lane's brief. The hook's purpose, an isolated feature branch that is
never the base branch, was already met, and the lane's coordinator accepted
the skip. The feature directory and this file were created by the specify
command itself, as Speckit always does.

## User Scenarios & Testing *(mandatory)*

The users are domain maintainers who publish a factory MCP declaration, and the
reviewers who validate one offline before a hosted server is accepted.

### User Story 1 - A hosted declaration carries a checked authorization block (Priority: P1)

A maintainer whose domain server is deployed declares the token profile that
server enforces: the issuer, the accepted algorithms, the audience and how it is
bound, and where the server's protected-resource metadata lives. The offline
validator refuses a hosted declaration that omits the block or states it
wrongly, while a stdio-only declaration needs none.

**Why this priority**: without the block nothing describes the tokens a hosted
server accepts, which is the gap the ruling *"RS256 baseline (Recommended)"*
answers. Every other story builds on the block existing.

**Independent Test**: validate synthetic declarations, one per scenario of
*Hosted declarations carry an authorization block*, and compare the stable
codes and locations the validator reports.

**Acceptance Scenarios** (delta requirement *Hosted declarations carry an
authorization block*):

1. **Given** a deployed service with no authorization block, **When** it is
   validated, **Then** it is refused with a stable code located at the service
   (*Hosted declaration without the block*).
2. **Given** a service that is not deployed because its server is reached only
   over stdio, **When** it is validated, **Then** no block is required, and a
   block that is present is refused (*Stdio-only declaration*).
3. **Given** a block whose issuer is not an absolute https issuer identifier,
   such as a bare runtime name, or carries a query, fragment or userinfo,
   **When** it is validated, **Then** the issuer is refused (*Issuer named
   rather than identified*).
4. **Given** a block whose metadata path differs from the RFC 9728 well-known
   location for the canonical resource URI, **When** it is validated, **Then**
   the path is refused (*Metadata off the well-known path*).
5. **Given** a deployed service whose canonical resource URI carries a query
   component, **When** it is validated, **Then** the resource URI is refused
   (*Hosted resource URI with a query*).
6. **Given** a block that cites neither evidence nor a gap for its claims,
   **When** it is validated, **Then** the block is refused, and a block
   supported only by a gap is reported valid-with-gaps, not verified
   (*Unsupported authorization claim*).

---

### User Story 2 - Every hosted server accepts RS256 (Priority: P1)

A maintainer lists the algorithms the server accepts. RS256 must be among
them, EdDSA may be added, and nothing else is admitted.

**Why this priority**: the estate's only live issuer signs RS256, so a hosted
server that omits it refuses every real token.

**Independent Test**: validate one hosted synthetic declaration per algorithm
list and compare the located codes.

**Acceptance Scenarios** (delta requirement *RS256 token-signing baseline*):

1. **Given** an algorithm list that omits RS256, for example EdDSA alone,
   **When** it is validated, **Then** the list is refused (*RS256 absent*).
2. **Given** a list that names `none`, HS256, HS384 or HS512 in any letter
   case, **When** it is validated, **Then** that entry is refused by name
   (*Unsigned or symmetric algorithm*).
3. **Given** a list naming RS256 and EdDSA, **When** it is validated, **Then**
   the list is accepted (*EdDSA beside RS256*).
4. **Given** a list naming another algorithm beside RS256, for example ES256,
   **When** it is validated, **Then** that entry is refused as not admitted by
   this profile (*An algorithm the profile does not admit*).

---

### User Story 3 - The audience is the server's own (Priority: P2)

A maintainer declares the one audience value the server requires, bound either
to the canonical resource URI or to an identifier the issuer assigned to this
resource alone.

**Why this priority**: one issuer serves every domain server, so only the
audience keeps a token for one server from being accepted by another.

**Independent Test**: validate hosted synthetic declarations, one per audience
case, and compare the located codes.

**Acceptance Scenarios** (delta requirement *Audience bound to the server's
own resource*):

1. **Given** a `resource_uri` binding naming the service's canonical resource
   URI, **When** it is validated, **Then** the binding is accepted (*Audience
   is the server's own resource*).
2. **Given** a `resource_uri` binding naming any other value, **When** it is
   validated, **Then** the audience is refused as unbound (*Audience names
   another resource*).
3. **Given** an issuer that writes an identifier it assigned to this resource
   into the token's audience, **When** the block binds the audience to that
   identifier, **Then** the binding is accepted, it rests on the block's cited
   evidence or gap, and validation does not certify it (*Issuer-assigned
   audience*).
4. **Given** an audience that contains a wildcard or equals the issuer
   identifier, **When** it is validated, **Then** the audience is refused
   (*Unbounded audience*).

---

### User Story 4 - Failures are classed by the inventory that reports them, in each domain's own vocabulary (Priority: P3)

A maintainer maps each status and code to a completed evaluation or an
execution failure. A dependency failure reported through the domain's error
inventory is an execution failure, and a result status is a completed
evaluation. Each domain keeps its own codes, and no neutral vocabulary is
imposed.

**Why this priority**: the validator already enforces this. The story pins the
enforcement with tests and makes the narrowed canon say what is enforced.

**Independent Test**: validate synthetic declarations that misclassify a code,
or share a code name across two domains, and compare the located codes. Show
the classification tests red against a mutant of `main`'s validator whose
classification comparison is removed.

**Acceptance Scenarios** (delta `## MODIFIED` requirement *Lossless results and
explicit failures*, and `## ADDED` requirement *Per-domain error vocabularies*):

1. **Given** a domain that reports through its error inventory that it cannot
   evaluate because a dependency is unavailable, **When** the mapping is
   validated, **Then** it identifies an execution failure and never eligible
   (*Unavailable dependency*, narrowed).
2. **Given** a result blocked by policy, **When** the mapping is validated,
   **Then** the blocked object is preserved as a completed evaluation
   (*Negative evaluation*, unchanged).
3. **Given** two domains whose error inventories each hold a code of the same
   name with different envelopes or retry semantics, **When** each declaration
   is validated, **Then** each maps its own code through its own inventory and
   the two codes are unrelated (*Two domains share a code name*).
4. **Given** a domain whose error inventory holds a code no other domain and no
   neutral list uses, **When** its declaration is validated, **Then** it is
   judged by its own mapping alone and not refused for the code's name (*A
   code no other domain uses*).

The MODIFIED requirement's third scenario, *Existing digested result*, is
carried unchanged by the delta and is outside this feature: no byte of its
enforcement moves.

### Edge Cases

- A structural fault inside the block (an unknown field, a wrong type, a
  binding outside the closed set, an empty or repeated algorithm list, an
  issuer given as a list or a second issuer field) is refused as `schema_oneOf`
  at `/service`. The structure pass does not descend into `service`'s `oneOf`
  branches, so the fault cannot name its field (`design.md` D7).
- A canonical resource URI that is already refused as `invalid_resource_uri`
  has no RFC 9728 location to derive, so the metadata path is not compared
  against it. The query check still applies, because a query is a fault of its
  own.
- An empty query (`https://mcp.example.test/mcp?`) is a query component, since
  RFC 3986 § 3 begins the query at the first `?`. A `?` inside a fragment is
  not a query, and the fragment is already refused.
- A canonical resource URI whose path is `/` derives the bare well-known path,
  exactly as an empty path does (`design.md` D4).
- `RS256` written in another letter case (`rs256`) is not RS256: algorithm names
  are case-sensitive (RFC 7515 § 4.1.1). Such an entry is not admitted, and RS256
  is then missing. Only the forbidden names compare without letter case.
- A `resource_uri` binding whose canonical resource URI itself contains `*` is
  refused: no audience may contain a wildcard, whatever its binding.
- A block's `evidence_ids` and `gap_ids` may each be empty in shape, as a tool's
  may. Citing nothing that carries `auth` is the semantic refusal
  `unsupported_auth`.
- A not-deployed declaration validates exactly as before. Its evidence and gap
  records may carry the new `auth` concern, which only adds an admitted value.
- Two declarations that name the same audience value are each validated alone,
  so a shared audience across domain servers cannot be detected offline. A
  `resource_uri` binding ties the audience to the server's own canonical
  resource URI. An `issuer_assigned` binding rests on the block's cited
  evidence or gap and is never certified (`design.md` D3).

## Requirements *(mandatory)*

### Functional Requirements

Each requirement traces to the delta scenario it serves (§ User Scenarios) and
to the design decision of the change that shapes it.

- **FR-001**: A declaration whose service is deployed MUST carry an
  authorization block, or be refused with `hosted_auth_missing` at `/service`
  (US1-1; D1, D7).
- **FR-002**: A not-deployed service MUST NOT carry the block. One that does
  MUST be refused with `schema_oneOf` at `/service`, as the closed branch refuses
  any unknown field today. A not-deployed declaration without a block MUST
  validate exactly as it does on `main` (US1-2; D1, D6).
- **FR-003**: The block MUST be closed and hold exactly six fields: one
  `issuer` string; a non-empty list of unique `algorithms` strings; one
  `audience` object of `binding` (the closed set `resource_uri` |
  `issuer_assigned`) and `value`; a `metadata_path`; and `evidence_ids` and
  `gap_ids` lists. No field may hold key material, a client secret or a token.
  Any break of that shape MUST be refused with `schema_oneOf` at `/service`
  (Requirement 1 body; D1, D7, OQ-6).
- **FR-004**: The issuer MUST be an absolute https URI with a host and no
  query, fragment or userinfo, or be refused with `invalid_issuer` at
  `/service/auth/issuer` (US1-3; D4).
- **FR-005**: The metadata path MUST equal `/.well-known/oauth-protected-resource`,
  followed by the canonical resource URI's path (as written in the URI, not
  decoded) when that path is neither empty nor `/`, or be refused with `auth_metadata_path_mismatch` at
  `/service/auth/metadata_path` (US1-4; D4, OQ-3).
- **FR-006**: A deployed service's canonical resource URI MUST carry no query
  component, or be refused with `auth_resource_query` at
  `/service/canonical_resource_uri`. The rule applies to deployed services only
  (US1-5; D4, OQ-3).
- **FR-007**: The block MUST cite at least one evidence or gap record carrying
  the new `auth` concern, or be refused with `unsupported_auth` at
  `/service/auth/evidence_ids`. Its ids MUST resolve as a tool's do: a repeated
  id is `duplicate_support_reference` at the list
  (`/service/auth/evidence_ids` or `/service/auth/gap_ids`), and a dangling id
  is `missing_support_reference` at its entry (`.../<k>`). The evidence and gap
  concern vocabularies MUST admit `auth`. A block supported only by a gap MUST
  be reported valid-with-gaps (US1-6; D5, OQ-4).
- **FR-008**: The algorithm list MUST name RS256, or be refused with
  `auth_rs256_missing` at `/service/auth/algorithms` (US2-1; D2).
- **FR-009**: An entry naming `none`, `HS256`, `HS384` or `HS512`, compared
  without letter case, MUST be refused with `auth_algorithm_forbidden` at
  `/service/auth/algorithms/<k>` (US2-2; D2).
- **FR-010**: Any other entry than exactly `RS256` or `EdDSA` MUST be refused
  with `auth_algorithm_unadmitted` at `/service/auth/algorithms/<k>`. RS256 with
  EdDSA MUST be accepted (US2-3, US2-4; D2, OQ-2).
- **FR-011**: A `resource_uri` binding MUST name exactly the canonical resource
  URI, or be refused with `auth_audience_unbound` at
  `/service/auth/audience/value` (US3-1, US3-2; D3).
- **FR-012**: An `issuer_assigned` binding MUST be accepted for any identifier
  of 1 to 2048 characters that no other audience rule refuses. Its support is
  the block's cited evidence or gap, and its validity MUST NOT certify it
  (US3-3; D3, OQ-1).
- **FR-013**: An audience value that contains `*`, or equals the issuer
  (compared exactly, as strings), MUST be refused with `auth_audience_unbound`
  at `/service/auth/audience/value`, whatever its binding (US3-4; D3).
- **FR-014**: An error-inventory code mapped as a completed evaluation, and a
  result-inventory status mapped as an execution failure, MUST each be refused
  with `outcome_classification_mismatch` at the mapping row. The enforcement
  exists on `main`. Its tests MUST be shown red against a mutant of `main`'s
  validator whose classification comparison is removed, and green against
  `main`'s own (US4-1, US4-2; D8).
- **FR-015**: The profile MUST define no neutral error-code vocabulary. Each
  declaration's codes MUST be read from its own pinned schema and never
  compared across declarations. A code name two domains share MUST carry no
  shared meaning, a code no other domain uses MUST NOT be refused for its name,
  and conformance MUST NOT require a domain to change a published schema
  (US4-3, US4-4; D9).
- **FR-016**: Every authorization check MUST run in the semantic pass, after
  structure and references, and report in the existing dimensions with the
  existing location, de-duplication, ordering and exit-code rules. A valid
  declaration MUST still report `verified_conformance: false` (Requirement 1
  body, last sentence; D7).
- **FR-017**: A deployed synthetic example declaration carrying a block MUST
  ship beside the existing not-deployed example, built only from synthetic
  identifiers (`tasks.md` 2.3; D7).
- **FR-018**: The runbook MUST describe the block, its codes, the stdio rule, the
  narrowed reading of *Unavailable dependency* and the per-domain vocabulary
  statement (`tasks.md` 2.5).
- **FR-019**: The declaration MUST be registered in the contract bundle for the
  first time, at the additive minor the cut allocates, with its digest, a
  `contracts/CHANGELOG.md` entry and `contracts/releases/<version>.digests.yaml`,
  in one candidate commit, under a claim of row 4 on #630. The text that calls
  the declaration unreleased (the schema's title and the runbook's release
  paragraph) moves to that version in the same commit. The version is
  allocated at the cut and never reserved (`tasks.md` 2.5, 2.6; D10, OQ-5).

### Key Entities

- **Authorization block**: the `auth` property of a deployed `service`. It
  describes the tokens the hosted server accepts and protects the existing
  `canonical_resource_uri`; it carries no second resource field.
- **Audience binding**: how the declared `aud` value is tied to this server,
  either `resource_uri` (the value is the canonical resource URI) or
  `issuer_assigned` (an identifier the issuer assigned to this resource alone).
- **The `auth` support concern**: a new key in the evidence and gap concern
  vocabulary. The block cites evidence or gap records by id, exactly as a tool
  cites its own.
- **Diagnostic codes**: nine new stable codes (`design.md` D7), plus two
  existing codes at new `/service/auth/...` locations, reported in the existing
  `structure` and `semantics` dimensions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Each of the 19 scenarios of the delta (16 ADDED, 3 MODIFIED) has
  at least one deterministic witness, or is recorded as carried unchanged and
  outside the feature (*Existing digested result*).
- **SC-002**: Each of the nine new codes in `design.md` D7, and each existing
  code at its new `/service/auth/...` location, has a test committed before any
  schema or validator change and shown failing against `main`'s validator.
- **SC-003**: The two characterization cases (a not-deployed service carrying a
  block, and a block-free stdio declaration) pass on `main` and on the branch.
- **SC-004**: The two classification tests fail against the mutant and pass
  against `main`'s own validator, and the verification record keeps both runs.
- **SC-005**: Every test `tests/factory-mcp/` held on `main` still passes,
  except where the ratified *Compatibility* section reverses its premise. Each
  such test is amended in the red-first commit and named in the verification
  record.
- **SC-006**: The full test suite and every gate CI runs show no new failure
  against `main` in the same clone kind, and any difference is explained in the
  verification record.
- **SC-007**: Two runs over the same synthetic inputs yield byte-identical
  reports.
- **SC-008**: The out-of-tree check against the engineering domain (`tasks.md`
  2.7), run by `--snapshot` only, finds that its hosted declaration reports
  `hosted_auth_missing` until its own slice declares a block (and
  `auth_rs256_missing` for a block that lists EdDSA alone), and that its stdio
  declaration validates as before. If it cannot be run, the verification
  record says it is owed.

## Assumptions

- Synthetic identifiers only: the `.test` and `.example` names RFC 2606 and
  RFC 6761 reserve. No real issuer, tenant, host or domain schema enters this
  public repository, and no codexFactory byte is vendored.
- No server runs, no token is minted and no network is reached. The validator
  stays offline, and tests block sockets.
- The version number is the coordinator's to claim on #630 (row 4) before the
  cut commit. `contract-v4.1` is the expected value only if no other cut lands
  first.
- The out-of-tree check against the engineering domain (`tasks.md` 2.7) runs
  only by `--snapshot` from a reviewer's own checkout. If it cannot be run here,
  it is recorded as owed.
- The profile declares what a hosted server enforces; it checks the
  declaration and never the tokens. Verifying a signature, finding keys
  (from the issuer's published metadata, which is public material, `design.md`
  D1), and checking expiry or other claims are the server's, at runtime. A
  valid block certifies none of them (Requirement 1, last sentence).
- The operations domain's DNS check landed callable-only, with no hosted
  declaration, so nothing of it changes (`design.md` *Compatibility*).
- This feature edits no file of the change packet under `openspec/changes/`.
  Ticking the packet's § 2 boxes is bookkeeping for the realization's landing,
  and the realization lands only on its own word, merged and green (`tasks.md`
  3.2).
- Out of scope, as the change's `tasks.md` § 5 lists: codexFactory's RS256
  slice, OpsxFactory's hosting-plan issuer correction, the Ops gateway's intake
  alignment, and any transport package, server, token minting or client
  registration.
