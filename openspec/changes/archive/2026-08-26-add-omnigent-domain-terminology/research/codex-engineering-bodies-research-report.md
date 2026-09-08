# Research report: software-engineering bodies — verified 2026-08-09

Run against live primary sources, answering
`codex-engineering-bodies-research-prompt.md`.

## Executive conclusion

Every candidate except O*NET fails the product-configuration reuse test.
This is the fourth domain in a row with the same result.

| Body | Verdict | Basis |
|---|---|---|
| **SWEBOK v4** | **Not usable** | IEEE permits educational/personal use free, but "permission to reprint/republish this material for commercial ... purposes or for creating new collective works for resale or redistribution must be obtained from IEEE" |
| **SFIA** | **Prohibited** | Established in the opsx round: no sub-licensing "through your products, services or associate, reseller and partner programmes" |
| **ISO/IEC/IEEE 12207** | **Not usable** | ISO sells its standards |
| **Scrum Guide** | **Not adopted** | CC BY-SA 4.0 — see below |
| **O\*NET** | **Adopted** | CC BY 4.0 with attribution |

## The share-alike question, answered

The 2020 Scrum Guide is licensed CC BY-SA 4.0. Share-alike means "if you
remix, transform, or build upon the material, you must distribute your
contributions under the same or compatible license."

The nuanced answer: **bare role and event names ("Sprint Review", "Scrum
Master") are very likely outside copyright** — individual words and short
titles generally are not protectable subject matter — so citing them would
probably not trigger share-alike. Reproducing the Guide's *definitional
text* would.

**Recommendation: do not adopt anyway.** The benefit is a label we can write
ourselves; the risk is a licence argument about whether our configuration
file became a derivative work obliged to be CC BY-SA. That trade is
asymmetric. Recorded in the registry as assessed-and-declined so the
reasoning is not lost.

## Verified O*NET codes (primary source: O*NET OnLine)

| Code | Title |
|---|---|
| 15-1252.00 | Software Developers |
| 15-1253.00 | Software Quality Assurance Analysts and Testers |
| 15-1251.00 | Computer Programmers |
| 15-1254.00 | Web Developers |
| 15-1243.00 | Database Architects |
| 15-1211.00 | Computer Systems Analysts |
| 27-3042.00 | Technical Writers (task statements verified verbatim) |

## Per-worker crosswalk applied

8 of 11 workers mapped at occupation level; 3 recorded `no_clean_equivalent`
— `pr_admission_agent`, `merge_readiness_agent`, `scrum_master_worker`.

`scrum_master_worker` is the notable one. It shares a name with a **human
role holding facilitation authority over people and process**. Rather than
map it, the overlay records `no_clean_equivalent` and its display label
deliberately avoids the term ("Process Flow Framing"). This is the same
hazard as O*NET's bookkeeper occupation including posting, but sharper,
because the authority in question is over people rather than records.

## Authority gap

Every O*NET occupation cited describes a whole human job that includes
**releasing and deploying**. Codex workers cannot merge or release — merge
authority belongs to GitHub branch protection and a human Merge Master. Each
note records what is not imported.

## Sources

- Scrum Guide (CC BY-SA 4.0): https://scrumguides.org/scrum-guide.html
- CC BY-SA 4.0 legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode
- SWEBOK v4: https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf
- IEEE CS SWEBOK page: https://www.computer.org/education/bodies-of-knowledge/software-engineering
- SFIA licensing: https://sfia-online.org/en/about-sfia/licensing-sfia/using-and-licensing-sfia
- O*NET family 15: https://www.onetonline.org/find/family?f=15
- O*NET 27-3042.00: https://www.onetonline.org/link/summary/27-3042.00
