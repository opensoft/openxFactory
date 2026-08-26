# Research report: IT-operations bodies — clean and lock

Status: record
Run: 2026-08-09 against live primary sources, answering
`opsx-it-operations-bodies-research-prompt.md`.

## Executive conclusion

**Both bodies opsx currently ships fail the reuse test.** This is the APQC
problem twice over, exactly as the brief anticipated:

1. **SFIA — prohibited.** The SFIA Foundation states plainly that "you cannot
   sub-licence SFIA to others through your products, services or associate,
   reseller and partner programmes", and lists "redistributing SFIA material
   in electronic or printed form to any other organisation (even if
   affiliated)" among restricted acts. Commercial product use requires a
   **SFIA Partner Licence** ("designed for organisations that wish to exploit
   SFIA commercially in support of the sale or delivery of products or
   services to customers"). Free use covers personal development and
   internal workforce management — not shipping codes in a public product
   repository. Our overlay ships `CHMG`, `CFMG` and `SCTY` today.
2. **ITIL — unverifiable permission, all rights reserved.** ITIL is a
   registered trade mark of PeopleCert (Axelos is now part of the PeopleCert
   group). The required acknowledgement is "ITIL® is a registered trademark
   of PeopleCert. All rights reserved." PeopleCert states that no part of
   its material "may be copied, distributed, disclosed or used other than as
   authorized by PeopleCert". Axelos' licensing pages did not render usable
   terms for third-party citation, so **no permission for our use could be
   established**. Treat as unlicensed until PeopleCert confirms in writing.
3. **COBIT — explicitly requires a licence.** ISACA: "A license is required
   for the incorporation of COBIT into software sold or given to third
   parties", and unauthorized uses include "inserting into ... any commercial
   or non-commercial product, including software". Do not adopt.

**Licence-clean replacements exist:**

4. **O\*NET — CC BY 4.0**, already adopted in the accounting domain on the
   same basis. Occupation codes verified directly on O\*NET OnLine.
5. **NIST CSF 2.0 — US Government work, public domain** under 17 USC 105.
   Version 2.0, published 2024-02-24. NOTE: the function names were **not**
   enumerated on the pages fetched, so no function-level mapping is proposed
   here; that requires one further verification against the framework PDF.
   Registering the body is safe; citing its internals is not yet verified.

## Verified O*NET occupation codes (primary source: O*NET OnLine)

| Code | Title |
|---|---|
| 15-1244.00 | Network and Computer Systems Administrators |
| 15-1212.00 | Information Security Analysts |
| 15-1231.00 | Computer Network Support Specialists |
| 15-1232.00 | Computer User Support Specialists |
| 15-1242.00 | Database Administrators |
| 11-3021.00 | Computer and Information Systems Managers |

Task statements were verified verbatim only for 11-3021.00. Mappings below
are therefore proposed at **occupation level**, marked partial, with
task-level verification outstanding.

## Verdicts on the shipped crosswalks

| Worker | Shipped | Verdict |
|---|---|---|
| ops_request_decomposer | itil4 | **Remove** — licence unverified |
| operation_planner | itil4 + sfia CHMG | **Remove both** — SFIA prohibited, ITIL unverified |
| readiness_validator | itil4 | **Remove** |
| inventory_agent | itil4 + sfia CFMG | **Remove both** |
| blast_radius_reviewer | itil4 `no_clean_equivalent` | Remove the body reference; the no-counterpart finding stands on its own |
| credential_grant_reviewer | itil4 `no_clean_equivalent` + sfia SCTY | **Remove both** |
| change_documentation_agent | itil4 | **Remove** |
| evidence_correlation_agent | itil4 | **Remove** |
| admission_packet_agent | itil4 | **Remove** |

The ITIL *analysis* recorded in those notes (e.g. that ITIL 4 assigns impact
assessment to the change authority within Change Enablement rather than to a
distinct practice) remains useful and is preserved in this report, but it
cannot ship as configuration content.

## Recommended replacement crosswalk (O*NET, occupation level)

| Worker | O*NET | Note |
|---|---|---|
| ops_request_decomposer | 15-1232.00 Computer User Support Specialists | Partial — request intake and scoping only |
| operation_planner | 15-1244.00 Network and Computer Systems Administrators | Partial — planning fragment; the occupation includes executing changes, this worker cannot execute |
| readiness_validator | 15-1244.00 | Partial — verification fragment, read-only |
| inventory_agent | 15-1244.00 | Partial — inventory and monitoring fragment |
| credential_grant_reviewer | 15-1212.00 Information Security Analysts | Partial — access review; no grant-issuing authority |
| evidence_correlation_agent | 15-1212.00 | Partial — monitoring and analysis fragment |
| blast_radius_reviewer | `no_clean_equivalent` | No IT occupation names impact-scope adjudication |
| change_documentation_agent | `no_clean_equivalent` | No verified occupation at this granularity |
| admission_packet_agent | `no_clean_equivalent` | Proposing to a human gate is a system control role, not an occupation |

**Authority gap, as in accounting:** every O\*NET occupation here describes a
whole human job that *includes executing changes*. These workers cannot
execute — execution is a human-approved act under a JIT grant, enforced by
GitHub branch protection and Azure/Kubernetes RBAC. Each note must say so.

## Recommendation

Remove ITIL and SFIA from the shipped overlay; adopt O\*NET at occupation
level with the authority gap recorded; register NIST CSF 2.0 as licence-clean
but do not cite its internals until the functions are verified; do not adopt
COBIT. Pursue a PeopleCert written permission or a SFIA Partner Licence only
if a client engagement requires ITIL or SFIA alignment — neither is worth a
licence for descriptive metadata.

## Sources

- SFIA licensing: https://sfia-online.org/en/about-sfia/licensing-sfia/using-and-licensing-sfia
- SFIA licensing overview: https://www.sfia-online.org/en/licensing-sfia
- PeopleCert acknowledgements: https://www.peoplecert.org/acknowledgements
- Axelos copyright and trade marks: https://www.axelos.com/legal/copyright-and-trade-marks
- ISACA COBIT usage guidelines: https://www.isaca.org/why-isaca/about-us/cobit-usage-guidelines
- ISACA COBIT commercial licensing: https://support.isaca.org/s/article/Can-I-license-COBIT-content-to-use-for-commercial-purposes-1597877236739
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- O*NET OnLine occupation family 15: https://www.onetonline.org/find/family?f=15
- O*NET 11-3021.00: https://www.onetonline.org/link/summary/11-3021.00
