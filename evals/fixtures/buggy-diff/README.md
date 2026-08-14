# buggy-diff fixture

A git diff with three known issues for the `code-review` skill eval:
1. An N+1 query (fetching users in a loop instead of a batch)
2. Missing error handling for empty results
3. A shotgun-surgery smell (one feature touches 5 files)

The agent reviews the diff against `HEAD` in this repo. Case `code-review-001`
checks whether the review is structured (two axes: Standards + Spec), catches
all three issues, and produces `docs/TODO.md`.

## Setup

This fixture is a git repo with the buggy change already committed on a feature
branch. The runner copies it and the agent reviews `git diff main..feature`.
See `cases/code-review.json`.
