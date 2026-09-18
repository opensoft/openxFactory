# Design: add-doxchat-model-intake

## The one question this document exists to answer

When a human types an API key into a wizard on a loopback dashboard, **where
does that string actually go?** Everything else in this change is small. This
is the decision that determines whether the change is conformant or is a
standing violation of the workspace's oldest rule.

Five designs were available. One is chosen. The other four are recorded with
the reason they were rejected, because a rejected option that is not written
down comes back as a "simplification" six weeks later.

## Chosen: the value transits to a declared credential broker and the dashboard keeps a binding

The intake flow carries the supplied value to the server, the server hands it
to the broker declared by `add-model-provider-broker`, and the dashboard
retains only the reference the broker returns, held in a record of the shape
`xfactory_credential_binding_template` already owns — `provider`,
`secret_ref`, `owner`, `rotation_policy`, optional `vault`. For the OAuth kind
the value never transits at all: the human is handed to the broker's own
authorization flow and the dashboard receives a reference, never a token.

**Why this one.**

1. **It is the only option with an existing ratified shape.**
   `credential-contracts` owns the binding template and the broker contract.
   The consumer-holds-a-binding-never-a-secret pattern is not being invented
   here; it is being applied to a consumer that lacks one.

2. **It makes the OAuth kind conformant rather than exceptional.** The
   `credential-contracts` requirement on worker credentials explicitly refuses
   to distribute "a refreshable session-state credential (one its consumer
   rewrites in place)" by any channel, on the grounds that an ephemeral copy's
   refresh silently stales the master. An OAuth refresh token is exactly that
   class. Every design in which the dashboard receives the refresh token
   violates this. The chosen design does not, because the refresh grant stays
   in one custody forever and only short-lived scoped material ever leaves it.

3. **It keeps this change small and honest about its dependency.** Custody,
   minting, and the provider client are `add-model-provider-broker`'s. This
   change adds the human intake and the approval seam and nothing else. The
   cost is that it cannot ship until that one does, which the sequencing
   requirement states outright rather than discovering at implementation time.

4. **It survives the negative fixtures already in the repository.** The
   credential validator rejects a `secret_ref` that looks like a raw secret
   (`sk-…`, `ghp_…`, `-----BEGIN`), and `contracts/avatar-client/redaction/
   denylist-patterns.yaml` carries a `provider_api_key` pattern for
   `sk-[A-Za-z0-9]{16,}`. A binding-only design has nothing for either to
   catch; the rejected designs below all have something.

**What it costs.** The flow is inert until openProfiler exists. This is a real
cost and the honest one — the alternative is shipping a wizard that works by
storing a secret somewhere forbidden, which is not a cheaper version of this
change but a different and worse one.

## Rejected: an OS keychain (libsecret / Keychain / DPAPI)

Superficially attractive: the platform already solves per-user secret storage,
the dashboard is loopback and single-user, and no new service is needed.

Rejected because:

- **No contract family covers it.** `credential-contracts` enumerates approved
  secret providers and the keychain is not among them. Adding it would be a
  contract change with a much larger blast radius than this feature, argued
  from the needs of a dropdown.
- **It has no answer to the accountability fields.** A grant is invalid
  without `issued_by`, `approved_by`, `expires_at`, and `audit_ref`. A keychain
  entry has none of these and no place to put them; it records that a secret
  exists, not that anyone authorized it.
- **It makes the dashboard a custodian.** The whole point of the binding
  pattern is that the consumer is not one. A keychain-backed dashboard holds
  the raw key at rest and reads it back on every turn, which is the posture
  the rule exists to prevent regardless of how good the storage is.
- **It does not travel.** Nothing about it works on a tenant install, and the
  second install would need the chosen design anyway — so the keychain buys a
  local shortcut at the price of building the real thing later, twice.

## Rejected: an environment variable the serve reads

The lowest-effort design: the wizard prints an export line, or writes one into
a state file the serve sources.

Rejected because:

- **The promoted requirement forbids even NAMING one.** The catalog "MUST NOT
  expose a provider credential, raw secret, raw endpoint, secret
  environment-variable name, or provider request template." A design whose
  central artifact is a secret environment-variable name is arguing with a
  ratified sentence.
- **The bridge already refuses to pass one.** `doxbench_bridge` inherits an
  ALLOWLIST of exactly `PATH`, `HOME`, `LANG`, `LC_ALL`, `TMPDIR` into the
  harness child, chosen as an allowlist precisely because "a denylist of
  credential-shaped names is a list somebody has to keep up with, and the one
  it misses is the one that leaks." Threading a provider key through would
  mean widening that allowlist, in a diff whose stated purpose is the opposite
  of why the allowlist exists.
- **It cannot work from a wizard anyway.** A process's environment is fixed at
  exec. A key entered in the browser cannot reach the running serve's
  environment without restarting the serve, so the wizard would end in
  "now restart your dashboard" — which is not the flow Brett asked for.

## Rejected: a SOPS-encrypted file in the checkout

`credential-contracts` explicitly blesses SOPS ciphertext with an externally
custodied decryption identity as an approved pattern, so this is the only
rejected option that is not simply forbidden.

Rejected because:

- **The precondition is the part the console does not have.** The pattern
  holds "only while every one of the following controls holds", and the
  load-bearing one is that "the private decryption identity lives durably only
  in an approved secret provider and is projected separately into the runtime
  decryption controller." A single-operator loopback console has no separate
  approved secret provider to custody the identity in. Put the identity beside
  the ciphertext and the ciphertext is a raw credential again, by the same
  requirement's own words.
- **It puts credential material in the corpus.** Every dashboard checkout
  becomes a ciphertext store, and the rotation rule — an exposed identity
  forces rotation of every credential ever encrypted to it, because historical
  git ciphertext stays recoverable — means a single mistake is unbounded in
  time.
- **It solves the wrong problem.** SOPS is for secrets a repository must carry
  to a deployment. This secret never needs to be in a repository at all.

## Rejected: the dashboard stores the key in its own plane state

Named only for completeness. `~/.local/state/xfactory-dashboard/` is outside
the checkout, so it would evade a repository grep and a commit hook.

Rejected because evading the detector is not the same as satisfying the rule.
This is the plain violation the standing rule names, and the fact that it
would pass the tests we happen to have written is an argument about our tests,
not about the design.

## The second decision: what "approved" means, and why intake must not decide it

Today approval is not a record. It is the conjunction of three runtime facts:
the entry is present in the `ModelCatalog` the install handed to
`model_port_factory`; `available` is true on it; and the console passed the
`session` verdict — `bool(actor and checkout_real and loopback)`. There is no
approver and nothing is written down.

That is defensible while the only way to add a model is to edit Python, since
whoever can do that is the operator by definition. **A wizard breaks the
implication.** If completing the flow set `available: true`, then supplying a
payment credential would be the same act as approving a provider to process
governed corpus material — and the placeholder the human is looking at says
"approved model", so the word is already making a promise.

So intake produces a PROPOSED declaration and approval is a separate, recorded
human act. This costs one extra click and buys the ability to answer "who
approved this model, when, and under what authority" — which is the same
question `credential-contracts` already forces every grant to answer.

**Consequence, stated because it is not free:** the gate-action record's
`action` enum is CLOSED, so the approval act needs an additive enum member and
therefore an additive contract bundle release. `add-doxbench-editing-phase-b`
hit this exact wall with `share-session` and recorded why reusing an existing
member fails: a governance record whose action is misnamed is worse than one
that does not exist. The same reasoning applies, so the same answer is taken.

## The third decision: the affordance does not ship early

The dropdown half of Brett's ask is genuinely small — an option element, an
ordering rule, and a default. It is tempting to ship it now and wire it later.

That is rejected. An "add model…" option that opens nothing is a worse state
than today's, because today the rail tells the human something true and
actionable, and the dead option would tell them the remedy is inside a control
where it is not. The sequencing is written as a requirement rather than left
as a note precisely so that the tempting half cannot be split off later by
someone who did not read this paragraph.
