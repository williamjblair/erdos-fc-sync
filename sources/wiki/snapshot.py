#!/usr/bin/env python3
"""Parse the frozen teorth/erdosproblems "AI contributions" wiki into a registry.

The wiki was frozen on 2026-06-30 ("no longer updated"). We commit the source
markdown alongside this script and re-derive registry.json from it here, so the
registry is reproducible offline and never silently drifts. erdos_frontier reads
only the committed JSON; it never clones the wiki at runtime.

Source: teorth/erdosproblems wiki, AI-contributions-to-Erdős-problems
        (wiki commit c8ad430, 2026-06-30).
"""

from __future__ import annotations

import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "AI-contributions.md"
OUT = HERE / "registry.json"

WIKI_COMMIT = "c8ad4309d20120c67cb97faa86daa1443acee018"
FROZEN_AT = "2026-06-30"
SOURCE = "teorth/erdosproblems wiki: AI-contributions-to-Erdős-problems"

COLOR = {"🟢": "green", "🟡": "yellow", "🔴": "red", "⚪": "white"}
PROB_RE = re.compile(r"\[\[(\d+)\]\]")
# "### 1(a). AI standalone"  /  "## 2. Secondary contributions"
SEC_RE = re.compile(r"^#{2,4}\s+(\d(?:\([a-d]\))?)\.\s*(.+?)\s*$")
# the formal-proof spine: primary contributions + 2(b) formalization.
SPINE_SECTIONS = {"1(a)", "1(b)", "1(c)", "1(d)", "2(b)"}


def _color_of(cell: str) -> str | None:
    for sym, name in COLOR.items():
        if sym in cell:
            return name
    return None


def _strip_colors(cell: str) -> str:
    for sym in COLOR:
        cell = cell.replace(sym, "")
    return cell.strip()


def _systems(cell: str) -> list[str]:
    return [s.strip() for s in cell.split(",") if s.strip()]


def _outcome(cell: str) -> dict:
    """Normalize an Outcome cell into {color, label, lean}."""
    return {
        "color": _color_of(cell),
        "label": _strip_colors(cell),
        # the wiki marks formalized contributions with a trailing "(Lean)".
        "lean": "(Lean)" in cell,
    }


def _split_row(line: str) -> list[str]:
    """Split a markdown table row into trimmed cells, tolerant of a missing
    trailing pipe (the wiki omits it on data rows)."""
    parts = [c.strip() for c in line.split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def parse(md: str) -> dict:
    lines = md.splitlines()
    section = section_name = None
    header: list[str] | None = None
    problems: dict[str, list[dict]] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = SEC_RE.match(line)
        if m:
            section, section_name = m.group(1), m.group(2).strip()
            header = None
            i += 1
            continue
        if line.startswith("| Problem"):
            header = _split_row(line)
            i += 2  # skip header + the |---| separator row
            continue
        if header is not None and line.lstrip().startswith("| [["):
            cells = _split_row(line)
            row = {header[j]: (cells[j] if j < len(cells) else "")
                   for j in range(len(header))}
            pm = PROB_RE.search(row.get("Problem", ""))
            if pm and section in SPINE_SECTIONS:
                entry = {
                    "section": section,
                    "section_name": section_name,
                    "ai_systems": _systems(row.get("AI systems", "")),
                    "date": row.get("Date", "").strip(),
                }
                if "Humans" in row and row["Humans"]:
                    entry["humans"] = _systems(row["Humans"])
                if "Literature" in row and row["Literature"]:
                    entry["literature"] = _strip_colors(row["Literature"]) or None
                if "Outcome" in row:
                    entry["outcome"] = _outcome(row["Outcome"])
                # 2(b): the contribution is formalizing an existing proof; the
                # color lives on the "Proof to formalize" cell, and the act
                # itself is a (Lean) formalization.
                if section == "2(b)":
                    ptf = row.get("Proof to formalize", "")
                    entry["proof_to_formalize"] = _strip_colors(ptf) or None
                    entry["outcome"] = {
                        "color": _color_of(ptf),
                        "label": "Formalization",
                        "lean": True,
                    }
                problems.setdefault(pm.group(1), []).append(entry)
            i += 1
            continue
        i += 1
    return problems


def summarize(problems: dict) -> dict:
    by_section: dict[str, int] = {}
    by_color: dict[str, int] = {}
    for entries in problems.values():
        for e in entries:
            by_section[e["section"]] = by_section.get(e["section"], 0) + 1
            c = (e.get("outcome") or {}).get("color")
            if c:
                by_color[c] = by_color.get(c, 0) + 1
    return {"problems": len(problems),
            "entries": sum(len(v) for v in problems.values()),
            "by_section": dict(sorted(by_section.items())),
            "by_color": dict(sorted(by_color.items()))}


def main() -> int:
    problems = parse(SRC.read_text(encoding="utf-8"))
    payload = {
        "schema": "erdos-ai-wiki-snapshot.v1",
        "source": SOURCE,
        "wiki_commit": WIKI_COMMIT,
        "frozen_at": FROZEN_AT,
        "note": "Frozen 2026-06-30; spine = sections 1(a-d) + 2(b) formalization. "
                "Secondary 2(a)/2(c)/2(d) (literature/rewriting/computation) link out.",
        "summary": summarize(problems),
        "problems": {k: problems[k] for k in sorted(problems, key=int)},
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    s = payload["summary"]
    print(f"wrote {OUT.name}: {s['problems']} problems, {s['entries']} entries")
    print(f"  by_section: {s['by_section']}")
    print(f"  by_color:   {s['by_color']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
