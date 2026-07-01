#!/usr/bin/env bash
# The whole batch session, one command:
#
#   bash scripts/ship.sh [batch-name]     (default: the first packeted batch)
#
# digest -> your verdict call (all-faithful, per-problem review, or quit)
#        -> sign (one key read) -> commit+push the signed state
#        -> assemble the FC branch -> confirm -> push + open the PR.
#
# Two decision points, both yours: the verdict call and the final y/N before
# anything leaves your machine for FC. Everything between is mechanical and
# was already gated (lake build, extract_names, link-rule, anti-collision).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"
FC_DIR="${FC_DIR:-$HOME/personal/formal-conjectures}"
STUB="packets/draft-review/verdicts_stub.json"

BATCH="${1:-$(python3 -c "
import yaml
c = yaml.safe_load(open('campaign.yaml'))
b = next((b['name'] for b in c['batches'] if b.get('state') == 'packeted'), '')
print(b)")}"
[ -n "$BATCH" ] || { echo "no packeted batch in campaign.yaml"; exit 1; }
PROBLEMS=$(python3 -c "
import yaml
c = yaml.safe_load(open('campaign.yaml'))
b = next(b for b in c['batches'] if b['name'] == '$BATCH')
print(' '.join(str(p) for p in b['problems']))")

echo "batch: $BATCH — problems: $PROBLEMS"

# regenerate packets + stub if missing (they are local artifacts)
if [ ! -f "$STUB" ]; then
  python3 match_packet.py --draft $PROBLEMS >/dev/null
  echo "(regenerated packets + stub)"
fi

# ---- the digest: one line per problem, the divergences that matter ----------
python3 - <<'EOF'
import json, pathlib
rows = json.load(open("packets/draft-review/verdicts_stub.json"))
print("\n--- digest -------------------------------------------------------------")
for r in rows:
    n = r["problem"]
    d = json.loads(pathlib.Path(f"statements/{n}/draft.json").read_text())
    notes = d.get("divergence_notes") or []
    first = (notes[0][:96] + "…") if notes and len(notes[0]) > 96 else (notes[0] if notes else "no divergences recorded")
    filled = r.get("verdict") or "·"
    print(f"  {n:>4} [{filled:^9}] {d.get('category','?'):15} {len(notes)} note(s) — {first}")
print("--------------------------------------------------------------------------")
print("full packets: packets/draft-review/erdos_<n>.md")
EOF

# ---- the verdict call --------------------------------------------------------
NEED=$(python3 -c "
import json
rows = json.load(open('$STUB'))
print(sum(1 for r in rows if r.get('verdict') not in ('faithful','variant','unfaithful')))")
if [ "$NEED" != "0" ]; then
  echo
  read -rp "sign [a]ll unfilled as faithful / [r]eview each packet / [q]uit: " ANS
  case "$ANS" in
    a|A)
      python3 - <<'EOF'
import json
p = "packets/draft-review/verdicts_stub.json"
rows = json.load(open(p))
for r in rows:
    if r.get("verdict") not in ("faithful", "variant", "unfaithful"):
        r["verdict"] = "faithful"
json.dump(rows, open(p, "w"), indent=2)
print("all verdicts set: faithful (your call, recorded under your key)")
EOF
      ;;
    r|R) bash scripts/sign-batch.sh --review; SIGNED=1 ;;
    *) echo "stopped — nothing signed."; exit 0 ;;
  esac
fi

# ---- sign (skip if --review already did) --------------------------------------
if [ "${SIGNED:-0}" != "1" ]; then
  bash scripts/sign-batch.sh "$STUB"
fi

# ---- commit + push the signed frontier state ----------------------------------
git add .vela/ frontier.json frontier.yaml vela.lock proof/ statements/ campaign.yaml 2>/dev/null || true
if ! git diff --staged --quiet; then
  git commit -q -m "Sign $BATCH fidelity verdicts"
  git push -q origin main
  echo "signed state committed + pushed (the verify gate re-derives it)."
fi

# ---- assemble the FC branch ----------------------------------------------------
python3 scripts/submit_batch.py assemble "$BATCH"

# ---- the outward step: one confirmation ----------------------------------------
BODY="statements/_batch-$BATCH-pr-body.md"
READY=$(python3 - "$BODY" <<'EOF'
import re, sys, pathlib
text = pathlib.Path(sys.argv[1]).read_text()
m = re.search(r"problems ([0-9, ]+)\.", text)
print(m.group(1) if m else "?")
EOF
)
BRANCH="erdos-campaign-$BATCH"
TITLE="ErdosProblems: add $READY (#3998 sync)"
echo
read -rp "push '$BRANCH' to your fork and open the FC PR titled '$TITLE'? [y/N]: " GO
if [ "$GO" = "y" ] || [ "$GO" = "Y" ]; then
  ( cd "$FC_DIR" \
    && git commit -q -m "$TITLE" \
    && git push -q -u fork "$BRANCH" \
    && gh pr create -R google-deepmind/formal-conjectures \
         --head "williamjblair:$BRANCH" --title "$TITLE" --body-file "$HERE/$BODY" )
  python3 - "$BATCH" <<'EOF'
import sys, yaml
name = sys.argv[1]
c = yaml.safe_load(open("campaign.yaml"))
for b in c["batches"]:
    if b["name"] == name:
        b["state"] = "pr-open"
yaml.safe_dump(c, open("campaign.yaml", "w"), sort_keys=False, allow_unicode=True)
EOF
  git add campaign.yaml && git commit -q -m "$BATCH: pr-open" && git push -q origin main
  echo "PR opened. The teorth bot moves the graph after merge; the daily join flips the buckets."
else
  echo "assembled but not pushed — the printed commands above work whenever you're ready."
fi
