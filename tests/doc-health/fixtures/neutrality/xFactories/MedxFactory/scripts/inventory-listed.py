#!/usr/bin/env python3
"""Fixture: medx-flavored tooling that IS inventoried.

Listed in stack.yaml's tooling surface and mentions the medx domain, so
neither uninventoried_tooling nor lexicon_absence may select it.
"""

MEDX_BANNER = "medx patient intake helper"

if __name__ == "__main__":
    print(MEDX_BANNER)
