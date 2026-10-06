# Codex compatibility baseline

Status: record
Kind: report
Lane: mcp-family-contract
Captured: 2026-09-07
Reduced: 2026-10-05, lane openxfactory-5 (openXfactory-5), opensoft/openxFactory#1242

Repository: codeXfactory/codexFactory (named opensoft/codexFactory when this
record was captured).
Inspected source revision: 4b12ba83add713666a94129fc45552d8989f8488.
This is a source observation, not artifact acceptance, runtime certification
or a change to the codex contract.

The codex MCP contract publishes three JSON Schemas. Their SHA-256 digests at
the revision above are:

| Schema role | SHA-256 |
| --- | --- |
| tool request | 2b443f76530de1528359c0d8c9d8ff7a45f82ebaa8c06ffa53c67a59897d5e3b |
| tool result | 907352c252dd14e569e5d388bebb6f36152ffe9be5e87b11ce4269f5a079426c |
| domain error | 590fb7f9db6a0cf6ad6a5bb15467ff5feae8ac748f99f0c2f78ec590f6854750 |

The proposed profile must leave codex schemas, outputs and client
compatibility unchanged (the ratified scenario *Existing tools*). It adds no
codex field, wrapper or dependency.

## Reduction note (2026-10-05)

codexFactory is a private repository and this one is public. As captured,
this record also summarized private internals: the schema files' paths inside
the source repository, the module paths and names of the implementation, a
description of how those modules behave, and the list of mapping questions
the codex side had not yet resolved. Those passages were removed when lane
openxfactory-5 brought this change onto main; the pull request that did so
lists them for the owner's disclosure decision. The original wording stays
reachable at d2baf6fd, the commit this change was brought over from. Nothing here vendors
codexFactory bytes; a reviewer with codexFactory access checks the digests
against the source with `--snapshot`, out of tree.

See the [design](../design.md) and [proposal](../proposal.md).
