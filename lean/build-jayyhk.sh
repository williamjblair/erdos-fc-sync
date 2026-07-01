#!/usr/bin/env bash
# Build Jayyhk/erdos-lean problem projects so `extract_assumptions.py --repo jayyhk`
# can audit them. Each `problems/<n>/` is its own lake project pinned to its own
# Lean toolchain + mathlib revision, so there is no single built env like plby.
#
# `lake exe cache get` shares the Mathlib olean download across projects on the
# same revision (a global cache), so building a whole toolchain GROUP costs one
# Mathlib download plus a per-file compile. Building all ~12 toolchain groups is a
# genuinely heavy job (each group is its own Mathlib); provision incrementally.
#
# Usage:
#   JAYYHK=~/personal/erdos-lean bash lean/build-jayyhk.sh [toolchain-substr ...]
# No args  -> build every problem project (heavy). One or more toolchain substrings
# (e.g. `v4.29.1 v4.27.0`) -> build only those groups (start with the ones your CI
# already provisions for plby / alphaproof, whose Mathlib is already downloaded).
#
# Sharding (for CI matrix jobs on the big toolchain groups): set SHARD_IDX and
# SHARD_TOT to split the (sorted) matching project list round-robin, e.g.
#   SHARD_IDX=0 SHARD_TOT=3 bash lean/build-jayyhk.sh v4.24.0
set -euo pipefail
JAYYHK="${JAYYHK:-$HOME/personal/erdos-lean}"
SHARD_IDX="${SHARD_IDX:-0}"
SHARD_TOT="${SHARD_TOT:-1}"
FILTERS=("$@")

match() {
  [ ${#FILTERS[@]} -eq 0 ] && return 0
  for f in "${FILTERS[@]}"; do case "$1" in *"$f"*) return 0;; esac; done
  return 1
}

built=0 skipped=0 i=0
for d in $(ls -d "$JAYYHK"/problems/*/ | sort); do
  [ -f "$d/lean-toolchain" ] || continue
  tc="$(cat "$d/lean-toolchain")"
  match "$tc" || { skipped=$((skipped+1)); continue; }
  if [ $(( i % SHARD_TOT )) -ne "$SHARD_IDX" ]; then i=$((i+1)); skipped=$((skipped+1)); continue; fi
  i=$((i+1))
  if [ -d "$d/.lake/build" ]; then echo "have  $(basename "$d")  [$tc]"; continue; fi
  echo "==>   $(basename "$d")  [$tc]"
  ( cd "$d" && lake exe cache get >/dev/null 2>&1 || true; lake build ) && built=$((built+1)) \
    || echo "!! build failed for $(basename "$d")"
done
echo "built $built project(s); $skipped filtered/other-shard. Now: python3 lean/extract_assumptions.py --repo jayyhk"
