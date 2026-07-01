#!/usr/bin/env python3
"""S0+S1 prep for the FC statement campaign: per problem, run the anti-collision
check, gather every drafting input, and stage a scaffold under statements/<n>/.

The mathematical act — writing the formal statement — is deliberately NOT done
here. This script prepares everything a drafter (human or agent) needs to do it
faithfully, and the fidelity gate (match packet + signed vsa_) judges the result.

Per problem it writes statements/<n>/:
  inputs.md    the verbatim problem LaTeX, the upstream state, the hosted
               theorem extract(s) with pinned URLs — the drafter's whole desk
  <n>.lean     a scaffold in FC house style (header, refs, namespace, attribute,
               docstring with the verbatim problem text) with the theorem left
               as `theorem erdos_<n> : sorry := by sorry` for the drafter
  draft.json   machine metadata: source hashes, hosted refs + SHAs, machine
               verdict, the formal_proof link decision, collision log

Usage:
  python scripts/draft_statement.py 24 93 164        # stage these problems
  python scripts/draft_statement.py --batch batch-3  # stage a campaign.yaml batch
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

import yaml

HERE = pathlib.Path(__file__).resolve().parent.parent
STATUS = HERE / "site" / "status.json"
CAMPAIGN = HERE / "campaign.yaml"
STAGING = HERE / "statements"
FC_REPO = "google-deepmind/formal-conjectures"
UA = {"User-Agent": "erdos-frontier-campaign"}

# Local clones preferred for hosted proof text (fast, already audited);
# fall back to raw.githubusercontent at the recorded URL.
LOCAL_SOURCES = {
    "plby": pathlib.Path.home() / "personal/lean-proofs-fork/src/v4.29.1/ErdosProblems",
    "jayyhk": pathlib.Path("/tmp/jayyhk/problems"),
}

APACHE_HEADER = """/-
Copyright 2026 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/
"""


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def collision_check(problem: int) -> dict:
    """Fresh per-problem anti-collision: open PRs touching the FC file + issues.

    Text search first (cheap), then file-level verification of any hit so a PR
    titled '31, 34, 47' does not falsely block problem 314.
    """
    out = {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "open_prs": [], "issues": []}
    prs = json.loads(subprocess.run(
        ["gh", "pr", "list", "-R", FC_REPO, "--search", f"ErdosProblems/{problem}",
         "--state", "open", "--json", "number,title"],
        capture_output=True, text=True, check=True).stdout or "[]")
    for pr in prs:
        files = subprocess.run(
            ["gh", "pr", "view", str(pr["number"]), "-R", FC_REPO,
             "--json", "files", "-q", ".files[].path"],
            capture_output=True, text=True).stdout
        if re.search(rf"ErdosProblems/{problem}\.lean\b", files):
            out["open_prs"].append({"number": pr["number"], "title": pr["title"]})
    issues = json.loads(subprocess.run(
        ["gh", "issue", "list", "-R", FC_REPO, "--search", f"in:title {problem}",
         "--state", "open", "--json", "number,title"],
        capture_output=True, text=True, check=True).stdout or "[]")
    out["issues"] = [i for i in issues
                     if re.search(rf"\b{problem}\b", i["title"])]
    return out


def hosted_theorem_extract(source: str, url: str, problem: int) -> dict:
    """The hosted proof's boxed theorem(s): local text preferred, pinned URL kept."""
    text, origin = None, url
    local = LOCAL_SOURCES.get(source)
    if local:
        cand = (local / f"Erdos{problem}.lean" if source == "plby"
                else local / str(problem) / f"Erdos{problem}.lean")
        if cand.exists():
            text, origin = cand.read_text(errors="ignore"), str(cand)
    if text is None:
        raw = (url.replace("github.com", "raw.githubusercontent.com")
                  .replace("/blob/", "/"))
        try:
            text = fetch(raw)
        except Exception as exc:  # noqa: BLE001 — record, don't die
            return {"source": source, "url": url, "error": str(exc)}
    # boxed/problem-numbered theorems + their doc comments, else first theorems
    thms = []
    pat = re.compile(r"(/--.*?-/\s*)?^(theorem|def)\s+(\S*erdos_?%d\S*|main_theorem|answer\S*)(.*?)(?=:=)" % problem,
                     re.M | re.S | re.I)
    for m in pat.finditer(text):
        thms.append(m.group(0).strip()[:2400])
    if not thms:
        for m in re.finditer(r"^theorem\s+(\w+).*?(?=:=)", text, re.M | re.S):
            thms.append(m.group(0).strip()[:2400])
            if len(thms) >= 2:
                break
    return {"source": source, "url": url, "origin": origin,
            "file_sha256": sha256(text), "theorems": thms}


def latex_sections(problem: int) -> dict:
    """The verbatim problem text + references from erdosproblems.com/latex/<n>."""
    text = fetch(f"https://www.erdosproblems.com/latex/{problem}")
    return {"raw": text, "sha256": sha256(text)}


def scaffold_lean(problem: int, latex_raw: str, state: str) -> str:
    category = "research solved" if any(
        s in (state or "") for s in ("proved", "disproved", "solved")) else "research open"
    # The problem statement body: everything up to the references/solution
    # commentary stays the drafter's judgment; we inline the raw LaTeX verbatim
    # as the docstring seed, marked for the drafter to trim to the boxed text.
    return f"""{APACHE_HEADER}
import FormalConjectures.Util.ProblemImports

/-!
# Erdős Problem {problem}

*References:*
- [erdosproblems.com/{problem}](https://www.erdosproblems.com/{problem})
<!-- DRAFTER: add cited papers from the solution line, [Xx00] style -->
-/

namespace Erdos{problem}

/--
<!-- DRAFTER: the boxed problem text VERBATIM from inputs.md (do not rephrase);
     for solved problems add the verbatim solution sentence + citations. -->
-/
@[category {category}, AMS 11]
<!-- DRAFTER: fix AMS tags; add `formal_proof using lean4 at "<pinned-url>"`
     ONLY if draft.json says link_allowed=true -->
theorem erdos_{problem} : answer(sorry) := by
  sorry

end Erdos{problem}
"""


def stage(problem: int, row: dict) -> dict:
    outdir = STAGING / str(problem)
    outdir.mkdir(parents=True, exist_ok=True)

    coll = collision_check(problem)
    if coll["open_prs"]:
        print(f"  !! {problem}: OPEN PR collision {coll['open_prs']} — refusing to stage")
        (outdir / "draft.json").write_text(json.dumps(
            {"problem": problem, "status": "blocked-collision", "collision": coll}, indent=2))
        return {"problem": problem, "status": "blocked-collision"}

    latex = latex_sections(problem)
    hosted = [hosted_theorem_extract(p["source"], p["url"], problem)
              for p in (row.get("proof_links") or [])]
    machine = row.get("machine") or {}
    link_allowed = machine.get("verdict") == "unconditional"

    inputs = [f"# Erdős Problem {problem} — drafting inputs\n",
              f"- upstream state: **{row.get('erdos_state')}**  ",
              f"- machine verdict: **{machine.get('verdict')}** (source {machine.get('source')})  ",
              f"- formal_proof link allowed: **{link_allowed}** (unconditional + signed vsa_ required)\n",
              "## Problem text (VERBATIM SOURCE — cite, do not rephrase)\n",
              "```latex", latex["raw"].strip(), "```\n"]
    for h in hosted:
        inputs.append(f"## Hosted theorem — {h['source']} ({h['url']})\n")
        if h.get("error"):
            inputs.append(f"_fetch error: {h['error']}_\n")
        for t in h.get("theorems", []):
            inputs.append("```lean\n" + t + "\n```\n")
    inputs.append("## Drafting rules\n"
                  "- Derive the statement from the problem text; the hosted theorems are a"
                  " shape prior. Record EVERY divergence between your statement and each"
                  " hosted theorem in draft.json divergence_notes.\n"
                  "- Category must match upstream state; verbatim docstring; erdos_<n>"
                  " naming; one @[category], AMS tags; sorry body.\n")
    (outdir / "inputs.md").write_text("\n".join(inputs))

    lean_path = outdir / f"{problem}.lean"
    if not lean_path.exists():   # never clobber a drafted statement
        lean_path.write_text(scaffold_lean(problem, latex["raw"], row.get("erdos_state")))

    meta = {
        "problem": problem,
        "status": "staged",
        "staged_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "upstream_state": row.get("erdos_state"),
        "latex_sha256": latex["sha256"],
        "machine_verdict": machine.get("verdict"),
        "machine_source": machine.get("source"),
        "link_allowed": link_allowed,
        "hosted": [{k: h.get(k) for k in ("source", "url", "file_sha256", "error")}
                   for h in hosted],
        "collision": coll,
        "divergence_notes": [],
    }
    (outdir / "draft.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"  ok {problem}: staged ({len(hosted)} hosted source(s), link_allowed={link_allowed})")
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("problems", nargs="*", type=int)
    ap.add_argument("--batch", help="stage a batch named in campaign.yaml")
    args = ap.parse_args()

    problems = list(args.problems)
    if args.batch:
        camp = yaml.safe_load(CAMPAIGN.read_text())
        batch = next((b for b in camp.get("batches", []) if b["name"] == args.batch), None)
        if not batch:
            sys.exit(f"batch {args.batch!r} not in campaign.yaml")
        problems += [p for p in batch["problems"] if p not in problems]
    if not problems:
        sys.exit("no problems given")

    rows = {r["problem"]: r for r in json.load(open(STATUS))["rows"]}
    results = []
    for n in problems:
        row = rows.get(n)
        if not row:
            print(f"  !! {n}: not in status.json")
            continue
        if row["bucket"] != "statement":
            print(f"  !! {n}: bucket is {row['bucket']!r}, not 'statement' — skipping")
            continue
        results.append(stage(n, row))
    staged = [r["problem"] for r in results if r.get("status") == "staged"]
    print(f"\nstaged {len(staged)}: {staged}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
