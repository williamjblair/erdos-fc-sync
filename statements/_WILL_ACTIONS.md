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

## 3. The batch-3 session — one command

```bash
bash scripts/ship.sh
```

It shows the ten-line digest (the key divergence per problem), asks once —
sign **[a]ll** as faithful, **[r]eview** each packet inline, or **[q]uit** —
then signs under your key, commits the signed state, assembles the FC branch,
and (after one y/N) pushes and opens the PR. Two keystrokes, both yours.
