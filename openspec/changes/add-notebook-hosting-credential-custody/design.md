# Design: add-notebook-hosting-credential-custody

Status: draft

Brett's ruling is the input; this records what the repository's own evidence
said when the ruling was checked against it, including the two places where the
evidence redirected the route.

## Ruling 1 — The by-reference discipline already exists, and it already refuses the shortcut

`credential-contracts` promotes "Worker credentials are distributed by reference
into ephemeral job scope" (`add-worker-credential-by-reference`, archived
2026-08-14, live on three Claude worker lanes — council-deliberation,
review-lane and doc-health-analysis). One clause in it decides more of this
change than the ruling anticipated:

> a refreshable session-state credential (one its consumer rewrites in place)
> SHALL NOT be distributed by any channel: it is the wrong class, because an
> ephemeral copy's refresh silently stales the master

**The `nlm` profile is exactly that class.** `~/.notebooklm-mcp-cli/profiles/
<name>/` holds cookies, a `csrf_token` and a `session_id` that the CLI rewrites
in place on refresh. So:

- The **password** (and a TOTP seed, if one exists) is a legitimate custody
  subject — long-lived material, the right class for a vault.
- The **session profile** is not, and must never become one. Copying it between
  xFactory and openXdox to save a login would be the precise defect this family
  already refuses, with the copy left implicit.

That makes Brett's ruling 2 — per-system authority, no shared ambient session —
independently required rather than merely preferred. The ruling reaches it from
accountability; the promoted requirement reaches it from credential class. Both
land on the same rule, which is why this change states it as a requirement
rather than as guidance.

An honest scope note: that requirement's subject is "a credential consumed by a
worker lane". The projection sync is plausibly such a lane, but the fit is by
analogy rather than by the requirement's own terms, so this change adds its own
requirement for operated identities instead of claiming the existing one
already covers the case.

A corroborating precedent worth recording: `xfactor-001` is already a governed
identity name in this estate, and already appears as a vault reference —
`vaultref://kv-opensoft-xfactory-qa/secrets/xfactor-001-claude-credentials-json`
(`ideation/staging/worker-host-app/`). The archived by-reference change's own
tasks name its successor as `xfactor-001-claude-credentials`, "token class NOT
the session file". The same identity family, the same vault, and the same
class distinction, arrived at independently a week earlier.

## Ruling 2 — The hook is half-present, so two ADDED requirements are owed, and nothing is MODIFIED

The route asked whether the ratified two-case custody requirement already
carries the hook. It carries HALF of it.

`add-notebook-projection-identity`'s generalization says: *"Contract artifacts
SHALL NOT hard-code the identity itself, its operator, or any credential for
it."* That is a PROHIBITION. It forbids the credential appearing in the wrong
place; it does not require the credential to be anywhere in particular. An
account whose password lives only in its creator's head satisfies it perfectly.

So the positive obligation is owed, and so is per-system authority, which the
generalization does not touch at all — it speaks of "the consuming
implementation" in the singular.

**Both are ADDED, and the generalization is deliberately NOT re-MODIFIED.** Two
reasons. First, `add-notebook-projection-identity` is ACTIVE and carries its own
MODIFIED delta on that exact requirement, ratified but unpromoted until it
archives on its migration evidence; a second active change modifying the same
requirement text would put two live deltas on one requirement. Second, the new
obligations are genuinely additive — custody and per-system authority are not
refinements of "who operates the vault", they are what happens after that
question is answered.

**A sequencing fact the ratification read should see:** these requirements
presume the generalization, which is ratified but not yet promoted. Until
`add-notebook-projection-identity` archives, the promoted `credential-contracts`
text still speaks only of the credential vault. Nothing breaks — the new
requirements stand on their own terms — but a reader of the promoted spec alone
will not see the operated-identity framing until that archive lands.

## Ruling 3 — The live bindings do not live here, and the repository says so in its own manifest

The route asked for the concrete binding instances on the credential-contracts
side. Checked against the repository, that is refused by an explicit residency
rule rather than by preference:

- `contracts/manifest.yaml`: *"openxFactory ships no instance records (they live
  in client installs, credential-contracts residency model)."*
- `docs/domain-factory-starter-pack.md`: *"Bindings belong to client or tenant
  deployments, not the domain repo. Domain repos provide templates only. Use
  secret references, never raw values."*
- `scripts/validate-credential-contracts.py` takes a `<domain-repo-path>` and
  scans that repo's `credentials/*.yaml` — it is "Run from the pinned
  openxFactory checkout, never copied into domain repos." The instances it
  validates are, by construction, elsewhere.

What openxFactory does hold is `examples/credential-contracts/
openxdox-dispatch.binding-template.example.yaml` — and its filename says what it
is. It names `provider: azure_key_vault`, `vault: kv-opensoft-xfactory-qa`,
`secret_ref: openxdox-intent-dispatch-app`, `owner: opensoft-platform`,
`rotation_policy: operator_managed`. Concrete values are legitimate THERE
because a packaged fixture is a fixture; the no-hard-coding rule binds contract
artifacts, lane definitions and domain repositories.

So the split: neutral obligations here, and no fixture (see the shape section
— a two-consuming-system example would trip `shared-secret-identity`); the live
xFactory sync-lane binding in the install's `credentials/` tree beside
`cir-opensoft-qa-dox-dispatch-minter`; the live openXdox binding as its own
successor packet in its own lane, exactly as the ruling already directs for
that half.

**This is flagged, not decided quietly.** The ruling asked for the instances
here; the repository's rule puts them there. If the ratifier prefers the
instances in openxFactory, the residency rule is what has to change first, and
that is a different and larger change.

## The binding shape these instances will use

Already published, so nothing is invented: `xfactory_credential_binding_template`
in `contracts/schemas/xfactory-credential-contracts.schema.yaml` requires
`[provider, secret_ref, owner, rotation_policy]` per binding, with `vault`
optional, under a `credential_bindings` map keyed by requirement id, inside a
`client` envelope. Two entries, one per consuming system, is the intended shape — but the
published record cannot yet carry what makes them two AUTHORITIES, and review
found two concrete reasons to say so plainly.

First, the binding object has NO consumer or access-identity field, and
`scripts/validate-credential-contracts.py` compares no authorities. Two
bindings naming the same vault principal validate cleanly. So the per-system
invariant is, today, held by review and estate wiring rather than proven by the
record; extending the shape is a `contracts/schemas/` change carrying the full
release ritual, and is named as an owed successor.

Second, the validator's `shared-secret-identity` check fires whenever two
bindings in one template share a `secret_ref` — and two consumers of ONE
account password is exactly that shape. The check exists to stop the dispatch
and content credentials collapsing into one, which is a different fault from
two consumers of one deliberately-shared identity, but it cannot tell them
apart. That is why no packaged fixture is added here: distinct references would
misrepresent the estate, and relaxing the rule is a change to a check with its
own good reason to exist.

## The contracts-or-not decision

**Nothing lands under `contracts/`, and no release ritual fires.** The
binding-template shape is already published, so there is no schema to add or
change, no `contracts/manifest.yaml` row, no digest, no
`contract_bundle_version` bump, no inventory rebuild, no verify-commit and no
tag. The bundle stays at `contract-v1.40`.

Decided on the same ownership test used for the hosting record, not on the cost
of the ritual: `contracts/` is schema-and-manifest territory whose members are
pinned by other repositories, and neither a neutral requirement nor a per-client
binding is that. The precedent is exact —
`add-worker-credential-by-reference`'s own packet was three files with no
contracts artifact, stating "No contract bundle was cut".

One realization consequence worth naming now: if a packaged fixture IS added
under `examples/credential-contracts/`, the self-test count string asserted in
`tests/credential_contracts/test_dispatch_credential_contract.py` ("3 positive
+ 5 negative") must be updated in the same commit, or the suite fails.

## What custody does not buy

Recorded here because the ruling demanded it be said rather than assumed away.

Holding the password governs WHO MAY OBTAIN IT and proves who did. It does not
make the sign-in unattended. `nlm login` drives a browser, sessions last roughly
twenty minutes, `--cdp-url` exists as a mechanism rather than a solution, and
Google may interpose 2FA or a device check whenever it likes. Automated login
remains future work gated on proving the flow end to end — the same posture this
thread already took for the manual share-approval lane and for the §12
share-API correction.

Two further honest limits: whether the account will enforce a second factor is
not yet known, so the TOTP seed the requirement provides for may or may not come
to exist; and authoring this change touches no live secret at all. Putting the
password into the vault is an operator's act performed under the landed rule and
evidenced per `credential-contracts` — not something this packet performs.
