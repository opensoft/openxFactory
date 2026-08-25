# doxBench Provider Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench can expose a server-declared model catalog through a narrow local provider port while keeping credentials, raw endpoints, and data-handling policy out of browser state.
Topics: doxbench, provider-boundary, ideation-dashboard, model-routing, privacy
Repository context: openxFactory doxBench model selection, data handling, and deployment boundary
Captured: 2026-07-28

## Possible feats

- **Policy-labelled model catalog** — Show available model labels, limits, and
  data-handling badges without exposing secrets or provider configuration.
- **Editor-only degradation** — Preserve the full local editing workflow when
  the allowlist is empty or every model is unavailable.

## Focus

This document isolates who chooses a model, where provider configuration lives,
and which deployment plane may send corpus material. Model choice is useful
only when it does not move credentials or routing policy into the browser.

## Proposed model

A same-origin catalog exposes opaque model ids, human labels, provider class,
input/output limits, availability, and a data-handling badge. The browser sends
only a selected catalog id. The server resolves it through a narrow injected
provider port and obtains credentials through the deployment's approved
server-side mechanism.

Catalog and turn routes are local human-console capabilities requiring a real
checkout, resolved actor, and console presence. A hosted model is listed only
after explicit deployment enablement and policy agreement. An empty catalog is
a supported editor-only state.

## Interfaces and boundaries

The provider boundary consumes a confined, validated chat turn and emits a
schema-checked response. It keeps raw credentials, secret names, endpoints,
provider templates, and provider payloads out of the browser, snapshots, chat
transcripts, git artifacts, gate records, logs, and errors.

The browser does not call a provider directly. The hosted/read-only dashboard
does not expose catalog, turn, editing, Apply, or Save controls until hosted
identity, model brokerage, and governed write application are separately
approved.

## Alternatives and tensions

- Browser-side bring-your-own keys simplify provider experimentation, but make
  credential and data-handling enforcement unreliable.
- Reusing a formal review-lane ensemble would avoid another adapter, but an
  interactive writing turn has different latency and governance semantics.
- A family-wide model gateway may eventually be valuable, but extracting one
  before a second consumer exists risks designing a platform around one UI.

## Open questions

- Which first local/on-tenant adapters satisfy the intended deployment
  environments?
- What evidence is sufficient for each catalog data-handling badge?
- At what second-consumer threshold should the narrow provider port become a
  neutral shared capability?

## Relationships

- The [grounded chat](doxbench-grounded-chat.md) defines the confined request
  delivered to this boundary.
- The [surface and scope](doxbench-surface-and-scope.md) determines when chat
  controls are reachable.
- The [governed runtime synthesis](doxbench-synthesis-governed-runtime.md)
  relates model access to write authority and deployment degradation.
- The current contract direction lives in the
  [ideation-dashboard delta](../../openspec/changes/add-workbench-integrated-editor-chat/specs/ideation-dashboard/spec.md).
