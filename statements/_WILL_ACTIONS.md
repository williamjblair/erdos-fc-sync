# Will's queue — campaign actions only you can take

## 1. Unblock #4345 (batch-2b: 31, 34, 47, 280) — 2 minutes

Smetalo asked "Does this resolve #469?" and it's sitting unanswered, which may
be why the PR has no review yet. #469 is an open request for problem 280, and
the PR adds `280.lean`.

Reply on https://github.com/google-deepmind/formal-conjectures/pull/4345:

> Yes — this adds `FormalConjectures/ErdosProblems/280.lean`, which is what
> #469 asks for. I've added "Closes #469" to the PR description so it links.

Then edit the PR body and append:

> Closes #469

## 2. Claim batch-3 on the umbrella issue — 1 minute

Comment on https://github.com/google-deepmind/formal-conjectures/issues/3998:

> Working on statements for Erdős problems 24, 93, 164, 314, 315, 333, 369,
> 401, 429, 435 (same conventions as #4319/#4343/#4345). Will open the PR once
> they're reviewed on my side.

## 3. When the batch-3 packets are ready (I'll tell you)

- Read `packets/draft-review/erdos_<n>.md` for each problem (the draft is
  inlined; judge it against the verbatim problem text).
- Fill `verdict` (+ `target` finding ids) in
  `packets/draft-review/verdicts_stub.jsonl`.
- Sign the batch in one key read:
  `vela attest . --batch packets/draft-review/verdicts_stub.jsonl --as reviewer:will-blair`
- Then: `python scripts/submit_batch.py assemble batch-3` and follow its three
  printed commands (commit, push, `gh pr create`).
