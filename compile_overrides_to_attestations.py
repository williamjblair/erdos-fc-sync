#!/usr/bin/env python3
"""Emit `vela attest faithfulness` commands from overrides.yaml.

Reads overrides.yaml and, for every entry that carries a `verdict:` key, PRINTS
the shell command a human would run to sign a statement-fidelity attestation.

This script signs nothing and calls no external tool. It only emits the commands
a human will review and run with their own key. Entries without a `verdict:` key
are skipped — they stay as ordinary dashboard overrides.

Usage:
    python compile_overrides_to_attestations.py [overrides.yaml]
"""

from __future__ import annotations

import shlex
import sys

from fc_sync_status import EPC, FC_REPO, load_overrides


KEY_PLACEHOLDER = "<your-signing-key>"
FORMAL_REF_PLACEHOLDER = f"{FC_REPO}@<sha>:ErdosProblems/{{problem}}.lean"


def attest_command(problem: int, entry: dict) -> str:
    verdict = entry["verdict"]
    reviewer = entry.get("reviewer") or "reviewer:<your-handle>"
    note = entry.get("reason") or entry.get("note") or ""
    formal_ref = entry.get("formal_ref") or FORMAL_REF_PLACEHOLDER.format(problem=problem)
    parts = [
        "vela",
        "attest",
        "faithfulness",
        "--target",
        f"vf_erdos_{problem}",
        "--verdict",
        verdict,
        "--informal-ref",
        f"{EPC.replace('https://www.', '')}/{problem}",
        "--formal-ref",
        formal_ref,
        "--note",
        note,
        "--reviewer",
        reviewer,
        "--key",
        KEY_PLACEHOLDER,
    ]
    return " ".join(shlex.quote(part) for part in parts)


def main(argv: list[str]) -> int:
    path = argv[1] if len(argv) > 1 else "overrides.yaml"
    overrides = load_overrides(path)
    emitted = 0
    print("# Generated from overrides.yaml entries carrying a `verdict:` key.")
    print("# This prints commands only; it signs nothing. Review, then run with your key.")
    print()
    for problem in sorted(overrides):
        entry = overrides[problem]
        if not entry.get("verdict"):
            continue
        print(f"# problem {problem}: {entry.get('reason') or entry.get('note') or ''}".rstrip())
        print(attest_command(problem, entry))
        print()
        emitted += 1
    if emitted == 0:
        print("# No overrides carry a `verdict:` key yet; nothing to emit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
