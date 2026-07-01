#!/usr/bin/env bash
# S2 mechanical gates for a staged statement draft.
#
#   bash scripts/gate_draft.sh <problem> [<problem> ...]
#
# For each problem: copy statements/<n>/<n>.lean into the FC checkout as the
# (new, untracked) FormalConjectures/ErdosProblems/<n>.lean, then
#   1. `lake build FormalConjectures.ErdosProblems.«<n>»` — compiles AND runs
#      the house linters (copyright / AMS / category / moduleDocstring; the lib
#      is globbed so no index edit is needed),
#   2. `lake exe extract_names <file> --no-docstrings` — the site metadata
#      extractor must see erdos_<n>,
#   3. the link-rule lint — a `formal_proof` attribute may appear iff
#      draft.json says link_allowed=true (machine-unconditional),
# writes statements/<n>/gates.json, and removes the copied file (it is
# untracked; statement-bucket problems have no FC file by definition).
#
# Env: FC_DIR (default ~/personal/formal-conjectures).
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
FC_DIR="${FC_DIR:-$HOME/personal/formal-conjectures}"

fail_all=0
for N in "$@"; do
  SRC="$HERE/statements/$N/$N.lean"
  DST="$FC_DIR/FormalConjectures/ErdosProblems/$N.lean"
  GATES="$HERE/statements/$N/gates.json"
  [ -f "$SRC" ] || { echo "!! $N: no draft at $SRC"; fail_all=1; continue; }
  if [ -e "$DST" ] && ! git -C "$FC_DIR" ls-files --error-unmatch "FormalConjectures/ErdosProblems/$N.lean" >/dev/null 2>&1; then
    rm -f "$DST"   # stale copy from an earlier gate run
  elif [ -e "$DST" ]; then
    echo "!! $N: FC already tracks $N.lean — not a statement-bucket problem"; fail_all=1; continue
  fi

  cp "$SRC" "$DST"
  build_ok=false; extract_ok=false; linkrule_ok=false
  build_log=$(cd "$FC_DIR" && lake build "FormalConjectures.ErdosProblems.«${N}»" 2>&1) \
    && build_ok=true
  if $build_ok; then
    extract_out=$(cd "$FC_DIR" && lake exe extract_names "FormalConjectures/ErdosProblems/$N.lean" --no-docstrings 2>/dev/null)
    echo "$extract_out" | grep -q "erdos_$N" && extract_ok=true
  fi
  # link-rule: formal_proof in the draft ⇔ link_allowed in draft.json
  has_link=false; grep -q "formal_proof" "$SRC" && has_link=true
  allowed=$(python3 -c "import json;print(json.load(open('$HERE/statements/$N/draft.json')).get('link_allowed',False))" 2>/dev/null || echo False)
  if [ "$has_link" = "true" ] && [ "$allowed" != "True" ]; then linkrule_ok=false
  else linkrule_ok=true; fi

  rm -f "$DST"
  python3 - "$GATES" "$build_ok" "$extract_ok" "$linkrule_ok" <<'EOF'
import json, sys, datetime
path, build, extract, linkrule = sys.argv[1:5]
json.dump({
  "gated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
  "build": build == "true", "extract_names": extract == "true",
  "link_rule": linkrule == "true",
  "passed": all(x == "true" for x in (build, extract, linkrule)),
}, open(path, "w"), indent=2)
EOF
  if $build_ok && $extract_ok && $linkrule_ok; then
    echo "ok $N: build+extract+link-rule green"
  else
    echo "!! $N: build=$build_ok extract=$extract_ok link_rule=$linkrule_ok"
    $build_ok || echo "$build_log" | tail -12
    fail_all=1
  fi
done
exit $fail_all
