# Statement staging

Drafts for the FC statement campaign live here, one directory per problem,
until they are signed and submitted. Nothing in this directory is truth — a
draft becomes an FC contribution only after it passes every gate:

    statements/<n>/
      inputs.md    the drafter's desk: verbatim problem LaTeX, upstream state,
                   hosted theorem extracts with pinned URLs (draft_statement.py)
      <n>.lean     the draft statement in FC house style (drafter edits this)
      draft.json   metadata + divergence notes + collision log
      gates.json   mechanical gate results (gate_draft.sh)

Lifecycle (see campaign.yaml for batch state):

1. `python scripts/draft_statement.py --batch <name>` — stages inputs +
   scaffold; refuses any problem with an open-PR collision.
2. The drafter writes the formal statement from the problem text (hosted
   theorems are a shape prior, never copied blindly) and records every
   divergence in draft.json `divergence_notes`.
3. `bash scripts/gate_draft.sh <n>` — copies into the FC checkout, `lake build`
   (compiles + house linters), extract_names check, link-rule lint.
4. `python match_packet.py --draft <n>` — the 3-panel fidelity packet; Will
   reviews, then signs the batch: `vela attest . --batch <stub> --as
   reviewer:will-blair`.
5. `python scripts/submit_batch.py <batch>` — assembles the FC branch from
   SIGNED drafts only; Will pushes and opens the PR.

A drafted `.lean` here is never edited after signing — post-sign changes
invalidate the vsa_ statement hash and must go back through the gate.
