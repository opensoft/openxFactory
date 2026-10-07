# Factory MCP Family Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Expose independently owned domain tools through common conformance rules, with OpsxFactory governing their hosting.
Topics: factory-mcp, mcp, domain-boundaries, contracts-versioning, hosted-domain-service-governance
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Establish a family MCP conformance profile and an Ops DNS pre-change callable contract, preserving existing codex behavior.
- Evaluate shared transport extraction after two domains prove equivalent needs.

## Motivation

Brett wants AI agents to work across software, infrastructure and medical
factories built from the same openxFactory model. A DNS change illustrates the
boundary: engineering patch inspection belongs to codexFactory; checking the
registered zone's proposed record state belongs to OpsxFactory. Hosting either
service does not transfer ownership of its tools.

## Goals

- Keep domain meaning and release ownership explicit.
- Give agents consistent descriptions of identity, scope, effects, outcomes,
  evidence and repetition.
- Preserve the two existing codex tools while testing a second domain.
- Produce a usable implementation boundary before committing to shared code.

## Non-goals

This packet is non-normative. It neither deploys a service nor ratifies a
contract. It does not add a universal executor, neutral listener, medical tool,
DNS writer, credential ceremony, release cut or consumer pin change.

## What the system delivers

The proposed first slice is a neutral conformance schema and validator, plus an
Ops-owned advisory DNS callable contract with synthetic-reader tests.
A successful DNS evaluation means the proposal passed planning checks against
the named observation. It does not mean approved, applied, propagated or still
valid after the world changes.

## System model

| Owner | Responsibility | Service direction |
| --- | --- | --- |
| openxFactory | Neutral declaration and conformance rules | No mandatory server |
| codexFactory | Engineering tools, contracts and implementations | Independent logical domain service |
| OpsxFactory | Infrastructure tools, including DNS checking | Independent logical domain service |
| MedxFactory | Future medical tools and domain safeguards | Independent logical domain service |
| Ops hosting governance | Accepted artifacts, ingress and deployment | Operates domain services without owning their meanings |

An agent can connect to several services. The host authenticates the caller,
resolves the binding, invokes a bounded domain capability and returns domain
evidence. A cross-domain workflow correlates evidence without transferring
permissions between domains.

## Cluster map

- [Domain services and shared conformance](factory-mcp-synthesis-family-surface.md)
  relates ownership, service identity and catalogs.
- [Trusted evaluation](factory-mcp-synthesis-evaluation-safety.md)
  relates scope, effects, evidence and replay/freshness.
- [Three-tool fit](factory-mcp-synthesis-three-tool-fit.md)
  compares existing codex behavior with the proposed DNS boundary.

## How it fits

openxFactory's existing neutral scope and credential vocabulary remains the
reference. New declaration fields live in a versioned conformance artifact,
not as invented MCP wire requirements. Domain schemas and results remain
domain-owned. Existing codex transport and hosting decisions retain their own
authority and lanes.

Proposed operational addresses include mcp.opsxfactory.opensoft.dev and
mcp.medxfactory.opensoft.dev alongside the codex domain address. These are
naming directions, not evidence of deployed endpoints. Brett's future .com
names need an explicit migration decision; the existing codex plan's production
naming is not amended here.

## Key decisions and open questions

Selected design: separate logical domain services; neutral conformance first;
no mandatory shared server; domain-specific payloads; advisory results; fresh
DNS observations; no extraction of the codex runner or replay mechanism.

Open for later integration: operational DNS readers and cancellation, host
identity/register resolution, revocation freshness, tenant partitions, audit
sink retention, deployment freshness limits, health probes and endpoint
migration. These do not need invented answers to build the bounded first slice.

The concrete proposals are
[add-factory-mcp-conformance](../../openspec/changes/archive/2026-10-06-add-factory-mcp-conformance/proposal.md)
and its separately owned Ops companion, add-dns-check-mcp. Ratification is a
separate act before implementation; see the neutral proposal for the paired
handoff.

## Document map

- Family surface: [ownership](factory-mcp-ownership.md),
  [service identity](factory-mcp-service-identity.md),
  [tool catalog](factory-mcp-tool-catalog.md).
- Evaluation safety: [trusted context](factory-mcp-trusted-context.md),
  [effects and authority](factory-mcp-effects-authority.md),
  [results and evidence](factory-mcp-results-evidence.md),
  [replay and freshness](factory-mcp-replay-freshness.md).
- Concrete fit: [codex mapping](factory-mcp-codex-mapping.md),
  [DNS check](factory-mcp-dns-check.md),
  [implementation boundaries](factory-mcp-implementation-boundaries.md).
