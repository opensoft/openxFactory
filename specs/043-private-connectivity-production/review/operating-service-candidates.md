# Operating service candidates for private connectivity production

Status: draft
Kind: review-packet
Prepared: 2026-11-14

This packet prepares C-02/C-04/C-08 choices from current read-only service and source inspection. It grants no operating authority, changes no frozen task definition and supplies no Q1–Q5 acceptance. The [commissioning register](../commissioning.md), [rollout gates](../rollout-gates.md) and [approval preparation register](production-approval-register.md) remain authoritative. All candidates need exact accepted ownership, compatibility and consuming-gate decisions before use.

## Existing Azure and identity candidates

This public coordination packet uses logical infrastructure roles. Exact subscription/resource identifiers, credential-delivery references and operating selectors belong in the accepted protected owner/target packet before execution. Public OIDC URLs are verification metadata, not credentials.

| Surface | QA candidate | Production candidate | Unclosed choice |
| --- | --- | --- | --- |
| Subscription | Existing Opensoft platform QA subscription | Existing Opensoft platform production subscription | Exact target, US West/US Central residency and operator acceptance |
| Private AKS | Existing private QA platform cluster, West US | Existing private production platform cluster, Central US | Dedicated service/customer scopes and actual schedulable capacity; no pool growth, eviction or shared-state adoption inferred |
| Container registry | Existing QA xFactory registry | Existing production platform registry | Exact repositories, actual supported immutable artifacts, promotion authority and readback |
| OIDC issuer | https://keycloak.opensoft.dev/realms/opensoft | https://keycloak.opensoft.one/realms/opensoft | Adopting caller declarations, exact audiences, signing compatibility and current governed application authorization |
| Public verification keys | https://keycloak.opensoft.dev/realms/opensoft/protocol/openid-connect/certs | https://keycloak.opensoft.one/realms/opensoft/protocol/openid-connect/certs | Exact issuer/JWKS binding and approved rotation/failure behavior |
| Secret-custody candidates | Existing QA xFactory vault | Existing production operations vault | Actual accountable owners, secret-specific access and approved delivery; no general vault role or credential values |
| Evidence-storage candidates | Existing QA xFactory storage account | Existing production archive account | Protected container-specific custody, writers/readers, immutable retention and actual authentication; no shared application/backup archive may be repurposed |

Both public opensoft discovery documents currently answer HTTP 200 with their matching canonical HTTPS issuer and endpoint URLs. This supersedes the older production handoff's statement that the opensoft realm was absent; it is an investigation observation, not application or rollout qualification. Source references: [QA endpoint runbook](https://github.com/opensoft/Opensoft-Tenant/blob/main/docs/runbooks/qa-keycloak-public-endpoint.md), [production handoff](https://github.com/opensoft/Opensoft-Tenant/blob/main/docs/runbooks/keycloak-prod-operational-handoff.md) and [separately governed production initialization](https://github.com/opensoft/Opensoft-Tenant/blob/main/specs/026-keycloak-browser-entrypoints/prod-initialization.md). No private administration, token issuance or identity mutation was attempted.

ARM readback reports QA blob versioning enabled, with blob/container deletion retention disabled. The inspected production archive reports 30-day blob/container deletion retention, but does not report versioning enabled. These settings do not establish a commissioned immutable evidence repository: the actual protected container, retention/immutability policy, access separation, redaction, output authentication and custodian are still C-08 decisions. Existing Keycloak, Hermes and customer backup containers are outside the proposed evidence allocation.

## Signing compatibility that must close before the real MCP path

The inspected MCP resource server's [token verifier](https://github.com/codeXfactory/codeXfactory/blob/main/packages/codexfactory-mcp-contract/src/codexfactory_mcp_contract/http/auth.py) accepts only EdDSA over Ed25519. Its second-algorithm path is explicitly a governed additive change. Current public JWKS metadata on both selected Keycloak realms exposes an RS256 signing key and an RSA encryption key; neither exposes an Ed25519 signing key. Advertising EdDSA in OIDC discovery does not provide an active usable Ed25519 signer, and a reachable issuer alone cannot qualify this workload.

Prepare a bounded additive Keycloak signing-configuration option for the new adopting callers, subject to the actual identity owner's accepted administrative plan: provide a usable Ed25519 realm key and client-specific EdDSA access-token selection while preserving the existing default and unrelated clients. Upstream [Keycloak release notes](https://www.keycloak.org/docs/26.5.7/release_notes/index.html) document EdDSA realm keys for client token signing, and its [OIDC configuration source](https://github.com/keycloak/keycloak/blob/main/server-spi-private/src/main/java/org/keycloak/protocol/oidc/OIDCConfigAttributes.java) names the client-specific access-token signature attribute. The installed provider/configuration, current administrative action class, owner authority and rollback/rotation plan must be verified before accepting this option. No key is generated and no issuer setting is changed here.

If that option cannot be authorized through the owning identity workflow, obtain a separate governed alternative before implementation or admission. Do not silently broaden the MCP algorithm allowlist, turn off verification, substitute synthetic credentials or declare the current RSA token path compatible. Actual issued-token verification, wrong issuer/audience/algorithm rejection, rotation and the approved real application control remain qualification requirements.

## Keep identity separate from authority

The existing [Ops identity administration workflow](https://github.com/opensoft/opsXfactory/blob/main/workflows/keycloak-administration.yaml) defines one realm per environment with organizations, identity/organization assertions only, authorization in the governed layer, and workload authority through credential contracts and openXwallet grants. It prohibits a realm split for isolation, role or membership as authority, workloads as realm users and unreviewed configuration. A population requiring stronger isolation uses a separately governed broker instance.

The proposed integration consumes those rules. A broker client declaration for an adopting caller does not make the MCP resource server an OAuth client, give it a client secret, grant product entitlement or authorize an Ops operation. MCP continues to consume public verification material and its trusted admitted-caller roster. Installer/customer authentication, current product entitlement, application admission and request-scoped Ops execution each need their own legitimate original subject and authority. Tenant/customer isolation must not be inferred from a Keycloak organization or network membership.

A production entitlement/current-revocation backend has not been identified in the inspected hosted-product source. The hosted owner must select and qualify the actual authoritative registry/journal and its access/custody contract before consumption. It must remain independent of restored Headscale/runtime snapshots and refuse stale or unavailable authority. A fixture entitlement, caller claim or restored old database cannot provide that proof. A new product-owned backend is a proposed missing piece, not an already commissioned Opensoft service.

## DNS, TLS, relay, platforms and limits

openxsoft.com uses Spaceship authoritative nameservers. No Azure DNS authority, API credential or DNS write is inferred. Prepare exact approved service/host/tenant boundaries and use the existing governed DNS/edge path only after its owner accepts the plan. QA has an observed Ready letsencrypt-prod issuer; that alone proves neither an issued openxsoft.com certificate nor private application TLS. Private MCP application ingress remains absent; unbound MCP has its own explicit application-authorized ingress policy. Select certificate custody, renewal and private reachability without exposing the private application as an ACME shortcut.

No production relay is selected or qualified by this packet. The package/hosted owners must choose the actual bounded relay/STUN endpoints, protocol/ingress behavior, region and outage/recovery policy, then verify direct, relay and disconnected behavior. No public relay-map fallback or additional public IP/load balancer spend is implied.

No dedicated available QA service volume or qualified Mac target has been identified. Brett approved preparation of a minimal dedicated-storage budget and investigation of GitHub macOS runners within included capacity with paid overages prohibited. The [storage budget](staging-storage-budget.md) and [Mac runner/billing guard proposal](macos-runner-options.md) make the next decisions concrete. Brett subsequently accepted the USD 10 storage-only financial envelope and authorized the now-applied repository Mac zero-paid guard. Actual provisioning and qualification remain gated; prepare actual per-target CPU/memory/storage/network/cost, data/fault/cleanup and observation/objective bounds before the remaining C-06/C-07 inputs and Q1 are accepted. Existing allocatable nodes, a versioned account and a reachable issuer cannot substitute for those inputs.

This packet changes neither source readiness nor live eligibility. Owner commissioning, the T010 bootstrap refinement and actual output authentication still precede their consumers; full Q0 and Q1–Q5 remain pending.
