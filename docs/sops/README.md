# openxFactory Standard Operating Procedures

Status: draft
Kind: process
Repository context: openxFactory

This directory owns repeatable operational procedures for openxFactory development,
qualification, installation, and incident handling.

SOPs may record credential requirement IDs, environment-variable contracts, secret
references, owners, and rotation procedures. They must never contain raw passwords, API
keys, tokens, private keys, or connection strings. Secret values remain in approved
secret providers or in explicitly permitted host-only development bindings.

## Catalog

| SOP | Purpose |
| --- | --- |
| [OpenAI Realtime F0 Lab Credential](openai-realtime-f0-lab-credential.md) | Provision, store, inject, verify, rotate, and revoke the lab credential used by the avatar brokered-call feasibility harness. |
| [Avatar Internal-Live Kill Switches](avatar-internal-live-kill-switch.md) | The named operator surface for the two server kill switches on the `gpt-realtime-2.1` internal-live ring: the two scopes, their block-new and revoke-active modes, the named holder, and the escalation path (`qualify-avatar-live-voice` §7.7). |
