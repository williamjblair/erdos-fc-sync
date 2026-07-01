#!/usr/bin/env python3
"""S5: post-merge bookkeeping for a campaign batch.

    python scripts/post_merge.py <batch> <merged-pr-url>

Appends a `defer` override row per problem (the 154/459 pattern: the FC file is
merged but the published conjectures.json lags a day, so the join must not
resurface the problem in NEXT_BATCH meanwhile), and marks the batch merged in
campaign.yaml. The daily join flips each problem to `done` once conjectures.json
reflects the merge; the teorth bot moves the public graph on its own.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent.parent
CAMPAIGN = HERE / "campaign.yaml"
OVERRIDES = HERE / "overrides.yaml"


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    name, pr_url = sys.argv[1], sys.argv[2]

    camp = yaml.safe_load(CAMPAIGN.read_text())
    batch = next((b for b in camp.get("batches", []) if b["name"] == name), None)
    if not batch:
        sys.exit(f"batch {name!r} not in campaign.yaml")

    over_text = OVERRIDES.read_text()
    added = []
    for n in batch["problems"]:
        if f"\n{n}:\n" in over_text or over_text.startswith(f"{n}:\n"):
            continue
        over_text += (
            f"\n{n}:\n"
            f"  bucket: defer\n"
            f"  reason: Campaign {name} PR merged; wait for conjectures.json to reflect it.\n"
            f"  source: {pr_url}\n")
        added.append(n)
    OVERRIDES.write_text(over_text)

    batch["state"] = "merged"
    batch["pr"] = pr_url
    CAMPAIGN.write_text(yaml.safe_dump(camp, sort_keys=False, allow_unicode=True))
    print(f"batch {name}: state=merged, defer overrides added for {added}")
    print("next: the daily join flips these to done once conjectures.json updates; "
          "then remove the defer rows (or they expire naturally when fc.linked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
