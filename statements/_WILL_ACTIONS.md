# Will's queue

The campaign state now lives in the frontier itself — no scripts, just vela.
The 10 batch-3 drafts are pending proposals in your inbox (created by
agent:claude, keyless; the engine refuses agents at every decision verb).

## The batch-3 session (pure vela, from this repo)

```bash
vela inbox .                          # the 10 pending statement proposals
vela diff <vpr_id>                    # inspect any one (drafts inline at
                                      #   statements/<n>/<n>.lean; divergence
                                      #   notes ride in each proposal)

vela accept-batch . --all-pending --reason "batch-3 statements reviewed" --dry-run
vela accept-batch . --all-pending --reason "batch-3 statements reviewed"

# fidelity verdicts: fill each "verdict" (faithful/variant/unfaithful) in
#   packets/draft-review/attest-batch3.json   (targets + hashes pre-filled)
# — or just tell Claude your verdicts and it fills the file — then:
vela attest . --batch packets/draft-review/attest-batch3.json --as reviewer:will-blair

git add -A && git commit -m "Accept + attest batch-3" && git push
```

After that, Claude assembles the FC branch with plain git and hands you the
`gh pr create` line (your account sends it). Claim the batch on FC #3998 first
if you haven't:

> Working on statements for Erdős problems 24, 93, 164, 314, 315, 333, 369,
> 401, 429, 435 (same conventions as #4319/#4343/#4345).

## Still open from before

- **#4345 unblock**: reply to Smetalo — yes, it resolves #469 (adds 280.lean);
  add "Closes #469" to the PR body.
- **#4343**: awaiting mo271 re-review (your fixes are pushed).
