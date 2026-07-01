#!/usr/bin/env python3
"""Lever 5 (OEIS lane): generate candidate OEIS links for Erdős problems that
have none, with evidence, for HUMAN verification — never submitted directly.

For each unlinked problem (upstream `oeis` empty/N/A), fetch its LaTeX text,
extract distinctive mathematical phrases, query the OEIS search API, and rank
hits. Output is a review file (packets/oeis/candidates.md + .json): each row is
problem -> candidate A-numbers with the sequence name and the phrase that
matched. Will verifies each candidate against the problem before any PR to
teorth/erdosproblems (data/problems.yaml).

Politeness: one OEIS query per second; --limit caps the tranche (default 40).

    python scripts/oeis_candidates.py --limit 40
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

import yaml

HERE = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = HERE / "packets" / "oeis"
UA = {"User-Agent": "erdos-frontier-oeis-lane (williamjblair)"}
ERDOS_URL = "https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml"

# phrases that define sequences (worth an OEIS query) vs generic math prose
PHRASE_RE = re.compile(
    r"(number of [a-z \-]{4,40}?(?:sets|numbers|integers|partitions|graphs|primes|ways|tuples|sequences))"
    r"|(smallest [a-z \-]{4,40}?(?:number|integer|prime|value))"
    r"|(largest [a-z \-]{4,40}?(?:number|integer|prime|value))"
    r"|((?:Sidon|Ramsey|covering system|sum-free|primitive|squarefree|practical|perfect|amicable|abundant|deficient|Ulam|Behrend|Davenport|van der Waerden|Schur) [a-z \-]{0,30}(?:set|sets|number|numbers|sequence|basis))",
    re.I)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def oeis_search(query: str) -> list[dict]:
    url = "https://oeis.org/search?fmt=json&q=" + urllib.parse.quote(query)
    try:
        doc = json.loads(fetch(url))
    except Exception:
        return []
    results = doc if isinstance(doc, list) else (doc.get("results") or [])
    return [{"anum": f"A{r['number']:06d}", "name": r.get("name", "")}
            for r in results[:4] if isinstance(r, dict) and "number" in r]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=40,
                    help="max problems to process this tranche")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    problems = yaml.safe_load(fetch(ERDOS_URL))
    unlinked = [p for p in problems
                if not [o for o in (p.get("oeis") or [])
                        if str(o).startswith("A")]]
    # prefer solved problems (their sequences are settled) and low numbers
    unlinked.sort(key=lambda p: (0 if "solved" in str(p.get("status", {}).get("state", ""))
                                 or "proved" in str(p.get("status", {}).get("state", ""))
                                 else 1, int(p["number"])))

    done_path = OUT_DIR / "processed.json"
    processed = set(json.loads(done_path.read_text())) if done_path.exists() else set()
    out_rows, checked = [], 0
    for p in unlinked:
        n = int(p["number"])
        if n in processed or checked >= args.limit:
            continue
        checked += 1
        processed.add(n)
        try:
            latex = fetch(f"https://www.erdosproblems.com/latex/{n}")
        except Exception:
            continue
        phrases = {m.group(0).strip() for m in PHRASE_RE.finditer(latex)}
        cands = []
        for ph in sorted(phrases)[:2]:            # max 2 queries per problem
            time.sleep(1.1)                        # OEIS politeness
            for hit in oeis_search(ph):
                cands.append({**hit, "matched_phrase": ph})
        if cands:
            out_rows.append({"problem": n,
                             "erdos_url": f"https://www.erdosproblems.com/{n}",
                             "state": (p.get("status") or {}).get("state"),
                             "candidates": cands})
            print(f"  {n}: {len(cands)} candidate(s)")

    done_path.write_text(json.dumps(sorted(processed)))
    (OUT_DIR / "candidates.json").write_text(json.dumps(out_rows, indent=2))
    md = ["# OEIS link candidates — for human verification\n",
          "Machine-suggested only. Verify each sequence actually IS the problem's",
          "object (check the OEIS entry's definition + references against the",
          "problem text) before adding it to teorth data/problems.yaml.\n"]
    for r in out_rows:
        md.append(f"## Problem {r['problem']} ({r['state']}) — {r['erdos_url']}\n")
        for c in r["candidates"]:
            md.append(f"- [{c['anum']}](https://oeis.org/{c['anum']}) — {c['name'][:110]}"
                      f"  \n  matched: _{c['matched_phrase']}_")
        md.append("")
    (OUT_DIR / "candidates.md").write_text("\n".join(md) + "\n")
    print(f"\n{len(out_rows)} problems with candidates -> {OUT_DIR}/candidates.md "
          f"({checked} processed this tranche)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
