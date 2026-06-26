# erdos-fc-sync

A **computed** source of truth for syncing solved-problem proofs into
[Formal Conjectures](https://github.com/google-deepmind/formal-conjectures).

## The problem: drift

An Erdős problem's "status" lives in several places that update independently:

- **erdosproblems.com** — the upstream status (open / solved / formally solved).
- **Formal Conjectures** — each file's `@[category ...]` annotation and `formal_proof` link.
- **[plby/lean-proofs](https://github.com/plby/lean-proofs)** — which solved problems have a
  hosted Lean proof, and whether it is conditional.

Reconciling these by hand is what drifts. The cost is double-work (two people formalising the
same problem) and mislabelling (a conditional proof linked as if it were complete).

## What this does

[`fc-sync-status.py`](fc-sync-status.py) computes the status instead of tracking it. It fetches
the three sources fresh, joins them on the problem number, folds in the live set of open FC pull
requests, and writes **[STATUS.md](STATUS.md)** — a per-problem worklist that can't go stale. A
GitHub Action regenerates it daily, so the link is always current.

## The status categories

| status | meaning |
|---|---|
| `statement` | a complete hosted proof exists, FC has no file — write the statement and link it |
| `link` | FC has the statement, the proof just isn't linked |
| `docstring` | the hosted proof is conditional or partial — note it in the docstring, not a `formal_proof` tag |
| `in-pr` | an open FC pull request already touches this file |
| `done` | already linked in FC |
| `no-proof` | no hosted Lean proof to link yet |

See **[STATUS.md](STATUS.md)** for the live lists, each linked to erdosproblems.com.

## Regenerate locally

```sh
pip install pyyaml
GH_TOKEN=$(gh auth token) python fc-sync-status.py
```

The token is only used to read open FC pull requests (the `in-pr` layer). Without it everything
else still computes.

## Context

This supports [formal-conjectures#3998](https://github.com/google-deepmind/formal-conjectures/issues/3998)
(syncing plby's proofs into FC) and #4184 (the Jayyhk set). It is offered as a coordination aid.
If the maintainers want it in-repo or wired into CI, the script is a single self-contained file.
