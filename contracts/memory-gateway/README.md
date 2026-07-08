# xFactory Memory Gateway Contracts

Status: standard
Kind: reference
Backed by: openspec/specs/memory-gateway/spec.md

This directory defines the product-neutral contracts for the xFactory Memory
Gateway. The gateway governs Customer Hermes memory and Domain Omnigent expert
memory/knowledge access before any provider I/O happens.

Canonical files in this directory:

- `vocabularies.yaml` defines the closed-set terms used by the gateway.
- `consent-profile.schema.yaml` is the first rail dependency for governed
  reads and context packets.
- `gateway-request.schema.yaml` and `gateway-response.schema.yaml` define the
  service-ready `xfactory.memory.*` operation frame.
- `provider-profile.schema.yaml`, `provider-binding.schema.yaml`, and
  `provider-mapping.schema.yaml` define provider capability, allowed route
  scope, credential custody, and traceability.
- `context-packet.schema.yaml` and `expert-context-packet.schema.yaml` define
  bounded runtime context for Customer Hermes and Omnigent experts.
- Lifecycle, safety, economics, portability, and audit contracts live in the
  remaining schema files.

Examples and conformance fixtures live under `examples/memory-gateway/`. They
are not canonical contracts, but they should validate against these shapes and
prove the rails-before-provider-I/O boundary.

Provider products may implement adapters, generated clients, smoke fixtures, or
runtime configuration elsewhere. Those implementation files are not canonical
unless this directory explicitly delegates ownership.
