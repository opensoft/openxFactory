# Co-residence finding — pre-ratification gate (design OQ-5, tasks 2.1)

Status: record
Date: 2026-08-21
Author: session finding for Brett Heap's ratification of `add-identity-brokering`
Question: does any current commitment imply a user population that must NOT
co-reside in a shared broker instance?

## Answer: YES — one population found

**HealthLinc patients.** The finding the gate exists to force: HealthLinc
(the branded patient frontend of the Medx family) carries a recorded
identity architecture in `xFactories/HealthLinc/docs/exec-summary.md` that
names Keycloak as its IdP with its own realm (`healthlinc-argentina`),
patient sign-up/sign-in/2FA handled there, and auto-provisioning of a
Frappe `User` + linked `Patient` document on first login. The population is
clinical patients — PHI-adjacent, per-deployment (regional), and owned by
the clinical surface, not by the operator. A patient persona has no
legitimate co-residence with the operator/staff persona plane: no operator
organization membership applies to it, no staff surface should resolve it,
and the blast radius of a shared-instance misconfiguration crosses a
clinical boundary.

**Disposition under design D3:** HealthLinc is pre-declared the FIRST
dedicated-instance client. Its recorded realm becomes a dedicated broker
INSTANCE realized through the per-client install pattern
(`xFactory-Keycloak-Install`, `config/clients/<tenant>/`) — which is
consistent, not in tension, with the single-realm ruling: that ruling
forbids realm-splitting *within the shared instance*; a dedicated instance
carrying its own realm is exactly the escalation path the contract's
silence on instance count exists to permit. The contract's silence is
therefore exercised at HealthLinc's go-live, not theoretically.

**Timing:** no live patient population exists today — HealthLinc's feature
001 (`one-patient-intake-experience`, ratified 2026-08-06) is built, and
the engine consumes verified session subjects (`healthlinc:<frappe user>`),
but no production patient base is recorded. There is consequently no
retroactive migration hazard and no ratification blocker: the finding
binds the *realization* (the shared instance MUST NOT be offered to
HealthLinc; the dedicated instance is provisioned before any patient
logs in).

## Candidates consulted, per the gate's naming requirement

1. **Medx clinical surfaces** — the population found (above). Also
   consulted: MedxEHR (clinician-side reconciliation overlay; a staff
   population with no recorded co-residence bar — and Medx's non-tenanted
   per-clinic deployment model already anticipates dedicated instances),
   and the medx-roottruth engine (no human login surface; service
   custody only).
2. **Business Central / FarHeap tenant work** — no barred population.
   FarHeap's identity runs in FarHeap's own Entra tenant (single-tenant
   app, `tenants/farheap.yaml`); its humans are tenant staff whose
   designed path is federation into the shared instance as the `farheap`
   organization with their own IdP. Nothing in the consent instrument,
   environment registrations, or grant evidence bars co-residence.
3. **DaVinciSite QA migration** (Opensoft-Tenant `docs/davincisite/`) —
   no barred population found; operator-run QA work with no end-user
   login population committed to any broker.

## Consequence recorded

The first dedicated-instance client exists before the first shared-instance
client does. Realization tasks must carry this as an acceptance condition:
the shared instance's client roster excludes clinical-patient populations
by rule, not by memory — the identity-brokering requirement that isolation
escalates by instance is the enforcement point.
