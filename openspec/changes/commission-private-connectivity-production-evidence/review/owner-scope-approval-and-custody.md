# Owner scope approval and remaining evidence custody decision

Status: ratified
Ratified: 2026-11-13 by Brett Heap. [Ratification record](ratification.md)
Kind: review
Decision date: 2026-11-13
Decision timezone: America/La_Paz

## Owner approval supplied in this session

Brett Heap gave this instruction:

> owner acceptance is approved. help me to T001-T005

T001–T005 were already completed and validated in [PR #1310](https://github.com/opensoft/openXfactory/pull/1310). This note records Brett's approval as the neutral/evidence maintainer of the reviewed coordinator E scope. He subsequently selected the prepared source-only C-08 policy below, completing the combined owner decision recorded in [ratification](ratification.md).

Reviewed source: [the published review-fix commit](https://github.com/opensoft/openXfactory/commit/d0452267972b5e5c0a468c862c1a4d7fbc451bdf). The reviewed T005 packet SHA-256 is 37d17ed5ee8570e542db9a2776f6c89a6d23d26c0ff069aa44d95179fe8dc008.

## Approved E scope

The scope is the exact nine surfaces in [design](../design.md#exact-proposed-surfaces), the T007–T010 verification commands in the reviewed [task list](../../../../specs/043-private-connectivity-production/tasks.md), and the closed task/case/instance contract identified by the review freeze:

- specs/043-private-connectivity-production/verify-evidence.py
- specs/043-private-connectivity-production/tests/test_evidence.py
- specs/043-private-connectivity-production/register-evidence-pins.py
- specs/043-private-connectivity-production/tests/test_evidence_pins.py
- scripts/doc_health/pin_class.py
- tests/doc-health/test_pin_reachability.py
- tests/doc-health/test_sentinel_vocabulary.py
- .github/workflows/pytest-suite.yml
- specs/043-private-connectivity-production/evidence/T010.json

Authority is bounded to this feature's E implementation under the completed T006 decision. Changed file/command/contract scope requires updated owner review. Neutral publication retains its separate T016 decision; other owner, release, target and Q0–Q5 decisions remain due at their own gates.

## Accepted source-only C-08 policy

After the policy was prepared for review, Brett selected: “Use the prepared source-only Git policy (Recommended).” The following source-only values are accepted for E bootstrap/source/CI evidence.

| Setting | Accepted value |
| --- | --- |
| Evidence custodian | Brett Heap, accountable for the E bootstrap and source-CI evidence |
| Durable binding | Reviewed, secret-free evidence exports and approval references in opensoft/openXfactory Git history, bound to exact immutable commit/content identities; accepted records land through the existing reviewed publication process |
| Retention | Project lifetime; preserve accepted observations and failed/blocked history, use new records for corrections or superseding decisions |
| Access | Existing repository permissions; publish only redacted source/CI material and references; credential, raw provider and customer payloads stay outside the public packet |
| Authentication | Exact source/receipt commit identities and SHA-256, actual GitHub repository/run/job identity and output references, plus Brett's review of actual output and human-decision provenance; a copied pass value supplies no approval |
| Scope | E bootstrap/source/CI only. Customer/provider/staging/production evidence requires its own protected custody decision before its consumer |

GitHub run/log references support provenance; durable reviewed exports preserve the required source results. This policy selects no cloud storage provider, paid resource, deployment permission or production data store.

Provider/customer/staging/production evidence requires a later protected-custody decision with its custodian, immutable binding, retention/access responsibility and authentication method before the relevant consumer.

## Current gate state

Owner E scope approval and the source-only C-08 selection are recorded above and in ratification.md. The E proposal is ratified, its origin approval metadata is populated and T006 is complete. T007 and later implementation remain unstarted. T001–T005 stay complete; full program Q0 is unaccepted and Q1–Q5 are not entered. The neutral publication proposal remains draft and PR #1310 stays draft.
